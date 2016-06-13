from fabric.api import env

host1 = 'root@10.204.217.172'
host2 = 'root@10.204.217.179'
host3 = 'root@10.204.216.111'
host4 = 'root@10.204.216.8'
host5 = 'root@10.204.216.11'
host6 = 'root@10.204.216.13'

kvm_nodei13 = '10.204.217.192'
kvm_nodei14 = '10.204.217.126'
kvm_nodek7 = '10.204.216.227'

ext_routers = [('hooper','10.204.217.240')]                                                                                                                                                             
router_asn = 64512                                                                                                                                                                                        
public_vn_rtgt = 2225                                                                                                                                              
public_vn_subnet = '10.204.221.160/28'
host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1,host2,host3,host4,host5,host6],
    'cfgm': [host1, host2],
    'webui': [host1],
    'openstack': [host1],
    'control': [host2, host3],
    'collector': [host1],
    'database': [host2],
    'compute': [host4, host5, host6],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodei13-vm2', 'nodei14-vm2', 'nodek7-vm2', 'nodea12', 'nodea15', 'nodea17']
}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host_build: 'stack@123',
}

reimage_param = os.getenv('REIMAGE_PARAM', 'ubuntu-14.04.2')

vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '16384',
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : ''http://10.204.217.158/images/node_vm_images/%s-256G.img.gz' % (reimage_param)',
                },
    host1 : {  
                'name' : 'nodei13-vm2',
                'server': kvm_nodei13,
                'network' : [{'bridge' : 'br1', 'mac':'52:53:55:01:00:02'}
                            ],
            },
    host2 : {   'name' : 'nodei14-vm2',
                'server': kvm_nodei14,
                'network' : [{'bridge' : 'br1', 'mac':'52:53:56:01:00:02'}
                            ]
            },
    host3 : {   'name' : 'nodek7-vm2',
                'server': kvm_nodek7,
                'network' : [{'bridge' : 'br1', 'mac':'52:53:57:01:00:02'}
                            ]
            }
}


minimum_diskGB=32
env.rsyslog_params = {'port':19876, 'proto':'tcp', 'collector':'dynamic', 'status':'enable'}
env.test_repo_dir='/home/stack/multi_interface_parallel/centos65/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.enable_lbaas = True
enable_ceilometer = True
ceilometer_polling_interval = 60
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.log_scenario='Multi-Node Virtual Testbed Sanity[mgmt, ctrl=data]'
