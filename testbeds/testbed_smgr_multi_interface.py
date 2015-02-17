from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'


#nodec33
host2 = 'root@10.204.221.59'

#nodec35
host1 = 'root@10.204.221.58'

#nodec60
#host3 = 'root@10.204.221.57'

#nodec57
host4 = 'root@10.204.221.61'

#nodea4
host5 = 'root@10.204.221.60'

#ext_routers = [('mx1', '10.84.17.253'), ('mx2', '10.84.17.252')]
ext_routers = []
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.46.0/24"
database_dir = '/home/cassandra'

host_build = 'root@10.204.216.4'

env.roledefs = {
    'all': [host1, host2, host4, host5],
    'cfgm': [host2, host1],
    'openstack': [host1],
    'control': [host2,host1],
    'compute': [host4, host5],
    'collector': [host2],
    'webui': [host2],
    'database': [host2],
    'build': [host_build],
}


env.hostnames = {
    'all': [ 'nodec35', 'nodec33', 'nodec57', 'nodea4']
}

env.password = 'c0ntrail123'

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host_build: 'contrail123'
}

bond= {
    host5 : { 'name': 'bond0', 'member': ['eth1','eth2','eth3','eth4'],'mode':'802.3ad' },
}

control_data = {
    host2 : { 'ip': '192.168.100.3/24', 'gw' : '', 'device':'eth1' },
    host1 : { 'ip': '192.168.100.4/24', 'gw' : '', 'device':'eth1' },
    #host3 : { 'ip': '192.168.100.5/24', 'gw' : '', 'device':'eth1' },
    host4 : { 'ip': '192.168.100.2/24', 'gw' : '', 'device':'eth1' },
    host5 : { 'ip': '192.168.100.1/24', 'gw' : '', 'device':'bond0' },
}


env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    #host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',

    host_build: 'stack@123',
}

multi_tenancy = True
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.test_repo_dir='/home/stack/smgr_github_multi_interface/contrail-test'
#env.mail_from='pbharat@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
#env.mail_to='dl-contrail-server-manager@juniper.net'
env.log_scenario='Server Manager Ubuntu-Icehouse Multi-Interface Sanity'
