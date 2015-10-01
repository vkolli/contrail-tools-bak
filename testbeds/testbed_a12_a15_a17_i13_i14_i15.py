from fabric.api import env

host1 = 'root@10.204.216.8'
host2 = 'root@10.204.216.11'
host3 = 'root@10.204.216.13'
host4 = 'root@10.204.217.125'
host5 = 'root@10.204.217.126'
host6 = 'root@10.204.217.127'

#ext_routers = [('hooper','192.168.193.253')]
#router_asn = 64512
#public_vn_rtgt = 2224
#public_vn_subnet = '10.204.221.192/28'
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
    'all': ['nodea12', 'nodea15', 'nodea17', 'nodei13', 'nodei14', 'nodei15']
}
#env.interface_rename = True

#control_data = {
#    host1 : { 'ip': '192.168.193.1/24', 'gw' : '192.168.193.254', 'device':'eth1' },
#    host2 : { 'ip': '192.168.193.2/24', 'gw' : '192.168.193.254', 'device':'eth1' },
#    host3 : { 'ip': '192.168.193.3/24', 'gw' : '192.168.193.254', 'device':'eth1' },
#    host4 : { 'ip': '192.168.193.4/24', 'gw' : '192.168.193.254', 'device':'p4p0p1' },
#    host5 : { 'ip': '192.168.193.5/24', 'gw' : '192.168.193.254', 'device':'p4p0p1' },
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

#env.ostypes = {
#    host1:'centos65',
#    host2:'centos65',
#    host3:'centos65',
#    host4:'centos65',
#    host5:'centos65',
#    host6:'centos65',
#}
env.cluster_id='clustera12a15a17i13i14i15'
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
#env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.log_scenario='Multi-Node Sanity[mgmt, ctrl=data]'
