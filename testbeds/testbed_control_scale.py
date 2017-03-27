from fabric.api import env

os_username = 'admin'
os_password = 'c0ntrail123'
os_tenant_name = 'demo'

# Management ip addresses of hosts in the cluster
host1 = 'root@10.87.64.129'
host2 = 'root@10.87.64.130'
host3 = 'root@10.87.64.131'
host4 = 'root@10.87.64.132'  # b4s342
host5 = 'root@10.87.64.133'  # b4s343
host6 = 'root@10.87.64.134'  # b4s344
#host4 = 'root@10.87.64.135'  # b4s376

# Host from which the fab commands are triggered to install and provision
host_build = 'root@10.87.64.129'  # b4s342

# External routers if any
ext_routers = [('mx-240', '6.6.6.10')]

# Autonomous system number
router_asn = 64512
public_vn_rtgt = 12345
public_vn_subnet = "10.84.42.0/24"

# Role definition of the hosts.
env.roledefs = {
    'all': [host1,host2,host3,host4, host5,host6 ],
    'cfgm': [host1,host2,host3],
    'openstack': [host1],
    'control': [host1,host2,host3],
    'compute': [host5, host6 ],
    'collector': [host1,host2,host3],
    'webui': [host1,host2,host3],
    'database': [host1,host2,host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['5b4s2','5b4s4','5b4s6','5b4s8', '5b4s10', '5b4s12', '5b4s14']
}

bond= {
    host1 : { 'name': 'bond0', 'member': ['em1','em2'], 'mode':'802.3ad' },
    host2 : { 'name': 'bond0', 'member': ['em1','em2'], 'mode':'802.3ad' },
    host3 : { 'name': 'bond0', 'member': ['em1','em2'], 'mode':'802.3ad' },
    host4 : { 'name': 'bond0', 'member': ['em1','em2'], 'mode':'802.3ad' },
    host5 : { 'name': 'bond0', 'member': ['em1','em2','em3','p2p1'], 'mode':'802.3ad' },
    host6 : { 'name': 'bond0', 'member': ['em1','em2','em3','p2p1'], 'mode':'802.3ad' },
}

control_data = {
    host1 : { 'ip': '5.5.5.129/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host2 : { 'ip': '5.5.5.130/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host3 : { 'ip': '5.5.5.131/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host4 : { 'ip': '5.5.5.132/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host5 : { 'ip': '5.5.5.133/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
    host6 : { 'ip': '5.5.5.134/24', 'gw' : '5.5.5.1', 'device' : 'bond0'},
}


static_route  = {
     host4 : [{ 'ip': '5.5.1.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.1', 'intf': 'bond0' }, {'ip': '6.6.1.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.2', 'intf': 'bond0' }],
     host5 : [{ 'ip': '5.5.1.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.1', 'intf': 'bond0' }, {'ip': '6.6.1.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.2', 'intf': 'bond0' }],
     host6 : [{ 'ip': '5.5.1.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.1', 'intf': 'bond0' }, {'ip': '6.6.1.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.2', 'intf': 'bond0' }],
}


# Passwords of each host
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
#    host4: 'c0ntrail123',

    host_build: 'c0ntrail123',
}

env.ha = {
    'contrail_internal_vip' : '5.5.5.250',
    'contrail_external_vip' : '10.87.64.250',
    'contrail_internal_virtual_router_id': 110,
    'contrail_external_virtual_router_id': 111,
}

#env.dpdk = {
#    host5: { 'huge_pages' : '75', 'coremask' : '0xff'},
#    host5: { 'huge_pages' : '75', 'coremask' : '0xff'},
#    host4: { 'huge_pages' : '75', 'coremask' : '0xff'},
#}

# For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
#    host4: 'ubuntu',
}
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


minimum_diskGB=32
env.test_repo_dir='/root/contrail-test'
