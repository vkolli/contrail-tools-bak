from fabric.api import env

host1 = 'root@10.204.217.133'
host2 = 'root@10.204.217.134'
host3 = 'root@10.204.217.135'
host4 = 'root@10.204.217.136'
host5 = 'root@10.204.217.137'

ext_routers = [('hooper','192.168.193.253')]
router_asn = 64512
public_vn_rtgt = 2224
public_vn_subnet = '10.204.221.192/28'
use_devicemanager_for_md5 = True
host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3,host4,host5],
    'cfgm': [host1],
    'webui': [host1],
    'openstack': [host1],
    'control': [host2, host3],
    'collector': [host1],
    'database': [host1],
    'compute': [host4, host5],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodei21', 'nodei22', 'nodei23', 'nodei24', 'nodei25']
}
env.interface_rename = True

control_data = {
    host1 : { 'ip': '192.168.193.1/24', 'gw' : '192.168.193.254', 'device':'eth1' },
    host2 : { 'ip': '192.168.193.2/24', 'gw' : '192.168.193.254', 'device':'eth1' },
    host3 : { 'ip': '192.168.193.3/24', 'gw' : '192.168.193.254', 'device':'eth1' },
    host4 : { 'ip': '192.168.193.4/24', 'gw' : '192.168.193.254', 'device':'p4p0p1' },
    host5 : { 'ip': '192.168.193.5/24', 'gw' : '192.168.193.254', 'device':'p4p0p1' },
}

env.openstack_admin_password = 'contrail123'
env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'centos65',
    host2:'centos65',
    host3:'centos65',
    host4:'centos65',
    host5:'centos65',
}
env.physical_routers={
'hooper'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'hooper',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.240',
             }
}

minimum_diskGB=32
env.test_repo_dir='/home/stack/multi_interface_parallel/centos65/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
multi_tenancy=True
env.interface_rename = True
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Multi-Interface Sanity[mgmt, ctrl=data]'
