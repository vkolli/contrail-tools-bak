from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'admin'

host1 = 'root@10.204.216.31'
host2 = 'root@10.204.216.30'
host3 = 'root@10.204.217.93'
host4 = 'root@10.204.217.94'
host5 = 'root@10.204.217.95'
host6 = 'root@10.204.217.96'

ext_routers = [('blr-mx1', '22.22.22.2')]
use_devicemanager_for_md5 = True
router_asn = 64510
public_vn_rtgt = 19005
public_vn_subnet = "10.204.219.88/29"

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6],
    'cfgm': [host1, host2],
    'openstack': [host2],
    'webui': [host3],
    'control': [host1, host3],
    'compute': [host4, host5, host6],
    'collector': [host1, host3],
    'database': [host1, host2, host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['nodea35', 'nodea34', 'nodec53', 'nodec54', 'nodec55', 'nodec56']
}

control_data = {

    host1: {'ip': '22.22.22.35/24', 'gw': '22.22.22.2', 'device': 'eth0'},
    host2: {'ip': '22.22.22.34/24', 'gw': '22.22.22.2', 'device': 'eth0'},
    host3: {'ip': '22.22.22.53/24', 'gw': '22.22.22.2', 'device': 'eth1'},
    host4: {'ip': '22.22.22.54/24', 'gw': '22.22.22.2', 'device': 'eth1'},
    host5: {'ip': '22.22.22.55/24', 'gw': '22.22.22.2', 'device': 'eth1'},
    host6: {'ip': '22.22.22.56/24', 'gw': '22.22.22.2', 'device': 'eth1'},
}

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

env.physical_routers={
'blr-mx1'     : {       'vendor': 'juniper',
                     'model' : 'mx',
                     'asn'   : '64512',
                     'name'  : 'blr-mx1',
                     'ssh_username' : 'root',
                     'ssh_password' : 'Embe1mpls',
                     'mgmt_ip'  : '10.204.216.253',
             }
}

minimum_diskGB=32
env.test_repo_dir = '/home/stack/regression/contrail-test'
env.mail_from = 'contrail-build@juniper.net'
env.mail_to = 'dl-contrail-sw@juniper.net'
multi_tenancy = True
env.interface_rename = True
env.log_scenario = 'MultiNode Regression'
env.enable_lbaas = True
do_parallel = True
