from fabric.api import env

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'demo'

# Management ip addresses of hosts in the cluster
host1 = 'root@10.87.64.132'  # b4s342
host2 = 'root@10.87.64.133'  # b4s343
host3 = 'root@10.87.64.134'  # b4s344
host4 = 'root@10.87.64.135'  # b4s376

# Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.64.132'  # b4s342

# External routers if any
ext_routers = []

# Autonomous system number
router_asn = 64512
public_vn_rtgt = 12345
public_vn_subnet = "10.84.42.0/24"

# Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host2, host3, host4],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5b4s8', '5b4s10', '5b4s12', '5b4s14']
}

control_data = {
    host1 : { 'ip': '5.5.5.132/24', 'gw' : '5.5.5.254', 'device':'bond0', 'vlan': '224'  },
    host2 : { 'ip': '5.5.5.133/24', 'gw' : '5.5.5.254', 'device':'bond0', 'vlan': '224'  },
    host3 : { 'ip': '5.5.5.134/24', 'gw' : '5.5.5.254', 'device':'bond0', 'vlan': '224'  },
    host4 : { 'ip': '5.5.5.135/24', 'gw' : '5.5.5.254', 'device':'bond0', 'vlan': '224'  },
}
# Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

# For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
}
minimum_diskGB = 256
do_parallel = False

# HA Test configuration
ipmi_username = 'ADMIN'
ipmi_password = 'ADMIN'

env.hosts_ipmi = {
    '10.87.64.132': '10.87.122.29',
    '10.87.64.133': '10.87.122.30',
    '10.87.64.134': '10.87.122.31',
    '10.87.64.136': '10.87.122.32',
}


env.test_repo_dir='/root/contrail-test/'

