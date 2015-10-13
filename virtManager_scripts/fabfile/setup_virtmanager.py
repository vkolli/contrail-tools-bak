import os
import fabric
from fabric.api import run,put,env,parallel
from fabric.operations import get, put
from fabric.context_managers import settings, hide
import re

env.hosts  = ['nodei12', 'nodei13','nodei14','nodei15']
env.user = 'root'
env.password = 'c0ntrail123'
env.no_keys = True

@parallel
def copy_virt_manager_script():
    if not fabric.contrib.files.exists('/root/tmp'):
        run('mkdir -p /root/tmp')
    if not fabric.contrib.files.exists("/root/tmp/InstallVirtManager.sh"):
        put('/cs-shared-test/cf/bin/InstallVirtManager.sh', '/root/tmp')

@parallel
def copy_image():
    if not fabric.contrib.files.exists('/root/tmp'):
        run('mkdir -p /root/tmp')
    if not fabric.contrib.files.exists("/root/tmp/std_ubuntu.img"):
        put('/cs-shared-test/images/std_ubuntu.img', '/root/tmp')

@parallel
def make_copy_of_image(num_of_copy):
    for i in range (int(num_of_copy)):
        image_name = 'image'
        image_name = '%s%s.img'%(image_name,str(i))
        run('cp /root/tmp/std_ubuntu.img /root/tmp/%s'%image_name)

def create_vm(name , image , ram = '4096',network = 'br0' , vcpus = '2',mac = ''):

    if not mac:
        cmd = 'virt-install --name %s \
            --ram %s \
            --disk %s \
            --network bridge=%s \
            --vcpus %s \
            --import \
            --graphics vnc' %(name,ram,image,network,vcpus)
    else:
        cmd = 'virt-install --name %s \
            --ram %s \
            --disk %s \
            --network bridge=%s,mac=%s\
            --vcpus %s \
            --import \
            --graphics vnc' %(name,ram,image,network,mac,vcpus)

    run (cmd)

def delete_vm( vm_id = ''):
    vm_dct = None
    if not vm_id:
        output = run('virsh list')
        vms = parse_virsh_list_output(output)
        for vm in vms:
            vm_id = vm[1]
            print vm_id
            cmd = "virsh destroy %s;virsh undefine %s"%(vm_id,vm_id)
            run(cmd)
    else:
        cmd = "virsh destroy %s;virsh undefine %s"%(vm_id,vm_id)
        run(cmd)

def parse_virsh_list_output(output):
    ret = []
    output = output.split('\r\n')
    values = output[2:]
    for v in values:
        ret.append((v.split()) )
    return ret

@parallel
def delete_images():
    cmd = 'rm -rf /root/tmp/*.img'
    run(cmd)
        

def create_file( f , text):
    try:
        with open (f , "w") as fl:
            fl.write(text)
    except Exception as e:
            self.logger.exception("Got exception while creating %s as %s"%(f,e))

def generate_etc_hostname(hostname):
    text = "%s"%hostname
    file_name = "hostname"
    create_file(file_name , text)

def generate_etc_hosts(hostname):
    file_name = "hosts"
    text = "127.0.0.1       localhost\n127.0.1.1       \
            %s.englab.juniper.net    %s"%(hostname,hostname)   
    create_file(file_name , text)
    
def change_host_name_of_vm(hostname):
    host = hostname
    generate_etc_hostname(host)
    generate_etc_hosts(host)
    run("cp /etc/hostname /etc/hostname.old")
    run("cp /etc/hosts /etc/hosts.old")
    put("hostname", "/etc/")
    put("hosts", "/etc/")
    run("reboot")

def change_libvirt_type(ty = 'qemu'):
    virt_file = run("cd /etc/nova;grep -r 'libvirt_type' *")
    f = virt_file.split(":")[0]
    f = "/etc/nova/%s"%f
    if fabric.contrib.files.contains(f, 'libvirt_type'):
        fabric.contrib.files.sed(f, 'libvirt_type.*=.*', 'libvirt_type=qemu',backup='.bak')
    else:
        fabric.contrib.files.append(f, 'libvirt_type=qemu')
    run("cat %s"%f)
    run ("service nova-compute restart") 

def chnage_head_less_mode(mode = 'true'):
    f = '/etc/contrail/contrail-vrouter-agent.conf'
    if fabric.contrib.files.contains(f, 'headless_mode='):
        fabric.contrib.files.sed(f, '.*headless_mode=.*', 'headless_mode=true',backup='.bak')
    run ("service supervisor-vrouter restart") 

def service_start_stop(service = 'supervisor-vrouter',action = 'stop'):
    run ("service %s %s"%(service,action)) 

@parallel
def run_virtmanager_manager_script():
    output = run('/root/tmp/InstallVirtManager.sh')

@parallel
def reboot_server():
    run('reboot') 

@parallel
def setup_bridge_interface():

    run('rm -rf /etc/network/interfaces')
    put( 'interfaces' , '/etc/network/')
    run('/etc/init.d/networking restart')


if __name__ == "__main__":
    copy_virt()
