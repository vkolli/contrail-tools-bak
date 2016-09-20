from fabric.api import env


host1 = 'root@10.204.216.15'
host2 = 'root@10.204.216.10'
host3 = 'root@10.204.217.209'
host4 = 'root@10.204.217.121'


ext_routers = [('blr-mx1', '10.204.216.253')]
router_asn = 64510
public_vn_rtgt = 19006
public_vn_subnet = "10.204.219.80/29"

host_build = 'stack@10.204.216.49'
#host_build = 'root@10.204.216.7'

env.roledefs = {
    'all': [ host1, host2,host3,host4],
    'cfgm': [host1],
    'openstack': [host1],
    'webui': [host1],
    'control': [host1],
    'collector': [host1],
    'database': [host1],
    'compute': [host2,host3,host4],
    'build': [host_build]
}

env.hostnames = {
    'all': ['nodea19', 'nodea14','nodel3','nodei9']
}

env.password = 'c0ntrail123'
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host_build: 'stack@123',
}

env.ostypes = {
    host1:'ubuntu',
    host2:'ubuntu',
    host3:'ubuntu',
    host4:'ubuntu',
}

env.orchestrator = 'openstack'
env.other_orchestrators={
'orch1'             :{
                         'name'         : 'vcenter',
                         'type'         : 'vcenter',
                         'vcenter_server': 'vcenter10',
                         'gateway_vrouters' : ['nodel3','nodei9'],
                         #'controller_refs'                : '' : if there are multiple 
                         #                                        contrail clusters,this entry point to
                         #                                        contrail cluster , this orchetrator rely on.
                        }
 }    

#env.slave_orchestrator = 'vcenter'
control_data = {
    host1 : { 'ip': '192.168.250.4/24', 'gw' : '192.168.250.254', 'device':'em1' },
    host2 : { 'ip': '192.168.250.5/24', 'gw' : '192.168.250.254', 'device':'em1' },
    host3 : { 'ip': '192.168.250.8/24', 'gw' : '192.168.250.254', 'device':'em2' },
    host4 : { 'ip': '192.168.250.19/24', 'gw' : '192.168.250.254', 'device':'p6p2' },
}

env.physical_routers={
'nodei9'     : {       
                     'name'  : 'nodei9',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.121',
                     'ports' : ['p6p1'],
                     'type'  : 'vcenter_gateway',
             },
'nodel3'       : {
                     'name'  : 'nodel3',
                     'ssh_username' : 'root',
                     'ssh_password' : 'c0ntrail123',
                     'mgmt_ip'  : '10.204.217.209',
                     'ports' : ['p514p2'],
                     'type'  : 'vcenter_gateway',
},
}

env.vcenter_servers = {
    'vcenter10': {
        'server':'10.204.217.189',
        'port': '443',
        'username': 'administrator@vsphere.local',
        'password': 'Contrail123!',
        'auth': 'https',
        'datacenter': 'a11a29',
        'cluster': ['a11a29_blr'],
        'dv_switch': { 'dv_switch_name': 'Distributed_Switch', 'nic': 'vmnic0', },
       # 'dv_port_group': { 'dv_portgroup_name': 'c4k4u14_dvpg', 'number_of_ports': '3', },
    },
}

esxi_hosts = {
    'nodel5' : {
        'ip' : '10.204.217.212',
        'username' : 'root',
        'password' : 'c0ntrail123',
        'cluster' : 'a11a29_blr',
        'datastore' : '/vmfs/volumes/l5-ds',
        'vcenter_server': 'vcenter10',
        'skip_reimage' : 'true',
        },
    'nodel6' : {
        'ip' : '10.204.217.215',
        'username' : 'root',
        'password' : 'c0ntrail123',
       'cluster' : 'a11a29_blr',
        'vcenter_server': 'vcenter10',
        'datastore' : '/vmfs/volumes/l6-ds',
        'skip_reimage' : 'true',
    },

}

minimum_diskGB=32
env.mail_from='contrail-build@juniper.net'
env.mail_to='sandipd@juniper.net'
multi_tenancy=True
env.interface_rename = False
env.encap_priority =  "'MPLSoUDP','MPLSoGRE','VXLAN'"
env.log_scenario='Vcenter Gateway'
env.enable_lbaas = True
do_parallel = True
env.ntp_server = 'ntp.juniper.net'

#enable ceilometer
enable_ceilometer = True
ceilometer_polling_interval = 60
env.test_repo_dir='/root/contrail-test-ci'
