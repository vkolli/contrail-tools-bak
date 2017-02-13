from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.204.217.194'
host2 = 'root@10.204.217.197'
host3 = 'root@10.204.217.198'

kvm_nodei33 = '10.204.217.145'

#External routers if any
#for eg. 
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = [()]
router_asn = 64520
#public_vn_rtgt = 30003
#public_vn_subnet = "10.204.219.0/29"


#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.204.217.187'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3],
    'cfgm': [host1],
    'control': [host1],
    'compute': [host2, host3],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
    'all': ['testbed-1-vm1', 'testbed-1-vm2', 'testbed-1-vm3']
}

#Openstack admin password
env.openstack_admin_password = 'contrail123'

env.password = 'c0ntrail123'
#Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    kvm_nodei33 : 'c0ntrail123',

    host_build: 'c0ntrail123',
}

#To enable multi-tenancy feature
multi_tenancy = False
minimum_diskGB=32
#To Enable prallel execution of task in multiple nodes
#do_parallel = True
#haproxy = True
env.log_scenario='Kubernets Sanity'

env.test = {
  'mail_to' : 'vjoshi@juniper.net',
  'webserver_host': '10.204.216.50',
  'webserver_user' : 'bhushana',
  'webserver_password' : 'bhu@123',
  'webserver_log_path' :  '/home/bhushana/Documents/technical/logs',
  'webserver_report_path': '/home/bhushana/Documents/technical/sanity',
  'webroot' : 'Docs/logs',
  'mail_server' :  '10.204.216.49',
  'mail_port' : '25',
  'mail_sender': 'contrailbuild@juniper.net',
}
vm_node_details = {
    'default': {
                'image_dest' : '/mnt/disk1/images/',
                'ram' : '16384',
                'vcpus' : '4',
                'disk_format' : 'qcow2',
                'image_source' : 'http://10.204.217.158/images/node_vm_images/centos-72-200G.img.gz'
                },
    host1 : {
                'name' : 'testbed-1-vm1',
                'server': kvm_nodei33,
                'network' : [{'bridge' : 'br1', 'mac':'52:54:00:01:00:01'}
                            ],
                'ram' : '16384',
                'vcpus' : '8',
            },
    host2 : {
                'name' : 'testbed-1-vm2',
                'server': kvm_nodei33,
                'network' : [{'bridge' : 'br1', 'mac':'52:54:00:01:00:02'}
                            ],
                'ram' : '8192',
                'vcpus' : '4',
            },
    host3 : {
                'name' : 'testbed-1-vm3',
                'server': kvm_nodei33,
                'network' : [{'bridge' : 'br1', 'mac':'52:54:00:01:00:03'}
                            ],
                'ram' : '8192',
                'vcpus' : '4',
            },
}
env.test_repo_dir='/root/vjoshi/contrail-tools/contrail-test'
env.orchestrator='kubernetes'
