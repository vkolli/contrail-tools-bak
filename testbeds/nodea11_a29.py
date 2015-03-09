from fabric.api import env

host1 = 'root@10.204.216.7'
host2 = 'root@10.204.216.14'
host3 = 'root@10.204.216.15'
host4 = 'root@10.204.216.25'
host5 = 'root@10.204.217.75'
host6 = 'root@10.204.217.4'

ext_routers = [('blr-mx1', '10.204.216.253')]
router_asn = 64512
public_vn_rtgt = 10003
public_vn_subnet = "10.204.219.80/29"

host_build = 'sandipd@10.204.216.4'


env.roledefs = {
    'all': [host1, host2, host3,host4, host5,host6],
    'cfgm': [host1,host2,host3],
    'webui': [host1],
    'openstack': [host1],
    'control': [host2, host3],
    'collector': [host1,host2],
    'database': [host1],
    'compute': [host4, host5, host6],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodea11', 'nodea18', 'nodea19', 'nodea29', 'nodeg35', 'nodec19']
}
#env.interface_rename = False
#
#control_data = {
#    host1 : { 'ip': '192.168.193.1/24', 'gw' : '192.168.193.254', 'device':'eth3' },
#    host2 : { 'ip': '192.168.193.2/24', 'gw' : '192.168.193.254', 'device':'eth3' },
#    host3 : { 'ip': '192.168.193.3/24', 'gw' : '192.168.193.254', 'device':'eth3' },
#    host4 : { 'ip': '192.168.193.4/24', 'gw' : '192.168.193.254', 'device':'eth3' },
#    host5 : { 'ip': '192.168.193.5/24', 'gw' : '192.168.193.254', 'device':'eth3' },
#}

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

env.ostypes = {
    host1:'centos',
    host2:'centos',
    host3:'centos',
    host4:'centos',
    host5:'centos',
    host6:'centos',
}
env.test_repo_dir='/home/stack/multi_interface_parallel/ubuntu/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='sandipd@juniper.net'
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Five node sanity'
env.enable_lbaas = True
