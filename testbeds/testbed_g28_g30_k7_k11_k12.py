from fabric.api import env

host1 = 'root@10.204.217.68'
host2 = 'root@10.204.217.69'
host3 = 'root@10.204.217.70'
host4 = 'root@10.204.216.227'
host5 = 'root@10.204.216.231'
host6 = 'root@10.204.216.232'

ext_routers = [('hooper','192.168.196.10')]
router_asn = 64512
public_vn_rtgt = 2226
public_vn_subnet = '10.204.221.144/28'

host_build = 'stack@10.204.216.49'

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6],
    'cfgm': [host1, host3],
    'webui': [host2],
    'openstack': [host3],
    'control': [host1, host3],
    'collector': [host1, host3],
    'database': [host1, host2, host3],
    'compute': [host4, host5, host6],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodeg28', 'nodeg29', 'nodeg30', 'nodek7', 'nodek11', 'nodek12']
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

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
    host5:'ubuntu',
    host6:'ubuntu',
}

control_data = {
    host1 : { 'ip': '192.168.196.1/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host2 : { 'ip': '192.168.196.2/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host3 : { 'ip': '192.168.196.3/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host4 : { 'ip': '192.168.196.4/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host5 : { 'ip': '192.168.196.5/24', 'gw' : '192.168.196.254', 'device':'eth1' },
    host6 : { 'ip': '192.168.196.6/24', 'gw' : '192.168.196.254', 'device':'eth1' },
}

env.cluster_id='clusterg28g29g30k7k11k12'
minimum_diskGB=32
env.test_repo_dir='/home/stack/multi-node/ubuntu/icehouse/contrail-test'
env.mail_from='contrail-build@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
env.interface_rename = True
multi_tenancy=True
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.log_scenario='MultiNode Multi-Interface Sanity'

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60
