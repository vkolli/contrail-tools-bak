from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@10.84.29.31'
host2 = 'root@10.84.29.32'
host3 = 'root@10.84.29.33'
host4 = 'root@10.84.29.34'
host5 = 'root@10.84.29.35'
host6 = 'root@10.84.29.36'
host7 = 'root@10.84.29.37'


#External routers if any
#for eg.
ext_routers = [('b6-mx80-4', '7.7.7.77')]
#ext_routers = []

#Autonomous system number
router_asn = 64513

#Host from which the fab commands are triggered to install and provision
host_build = 'root@10.84.29.31'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2,host3, host4, host5, host6, host7],
    'cfgm': [host1, host2, host3],
    'openstack': [host1,host2, host3],
    'webui': [host1, host2, host3],
    'control': [host1, host2, host3],
    'compute': [host4, host5, host6, host7],
    'collector': [host1, host2, host3],
    'database': [host1, host2, host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['b7s31', 'b7s32','b7s33','b7s34', 'b7s35', 'b7s36', 'b7s37']
}
#Openstack admin password
env.openstack_admin_password = 'c0ntrail123'

# Passwords of each host
# for passwordless login's no need to set env.passwords,
# instead populate env.key_filename in testbed.py with public key.
env.passwords = {
    host1: 'c0ntrail123',
    host2: 'c0ntrail123',
    host3: 'c0ntrail123',
    host4: 'c0ntrail123',
    host5: 'c0ntrail123',
    host6: 'c0ntrail123',
    host7: 'c0ntrail123',
    host_build: 'c0ntrail123',
}

# SSH Public key file path for passwordless logins
# if env.passwords is not specified.  
#env.key_filename = '/root/.ssh/id_rsa.pub'

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
    host6: 'ubuntu',
    host7: 'ubuntu',
}
#env.orchestrator = 'openstack' #other values are 'vcenter', 'none' default:openstack

#ntp server the servers should point to
#env.ntp_server = 'ntp.juniper.net'

# OPTIONAL COMPUTE HYPERVISOR CHOICE:
#======================================
# Compute Hypervisor
#env.hypervisor = {
#    host5: 'docker',
#    host6: 'libvirt',
#    host10: 'docker',
#}
#  Specify the hypervisor to be provisioned in the compute node.(Default=libvirt)

# INFORMATION FOR DB BACKUP/RESTORE ..
#=======================================================
#Optional,Backup Host configuration if it is not available then it will put in localhost
#backup_node = 'root@2.2.2.2'

# Optional, Local/Remote location of backup_data path
# if it is not passed then it will use default path
#backup_db_path= ['/home/','/root/']G
#cassandra backup can be defined either "full" or "custom"
#full -> take complete snapshot of cassandra DB
#custom -> take snapshot except defined in skip_keyspace
#cassandra_backup='custom'  [ MUST OPTION]
#skip_keyspace=["ContrailAnalytics"]  IF cassandra_backup is selected as custom
#service token need to define to do  restore of backup data
#service_token = '53468cf7552bbdc3b94f'


#OPTIONAL ANALYTICS CONFIGURATION
#================================
# database_dir is the directory where cassandra data is stored
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/data
#
#database_dir = '<separate-partition>/cassandra'
#
# analytics_data_dir is the directory where cassandra data for analytics
# is stored. This is used to seperate cassandra's main data storage [internal
# use and config data] with analytics data. That way critical cassandra's
# system data and config data are not overrun by analytis data
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/data
#
#analytics_data_dir = '<separate-partition>/analytics_data'
#
# ssd_data_dir is the directory where cassandra can store fast retrievable
# temporary files (commit_logs). Giving cassandra an ssd disk for this
# purpose improves cassandra performance
#
# If it is not passed, we will use cassandra's default
# /var/lib/cassandra/commit_logs
#
#ssd_data_dir = '<seperate-partition>/commit_logs_data'

#following variables allow analytics data to have different TTL in cassandra database
#analytics_config_audit_ttl controls TTL for config audit logs
#analytics_statistics_ttl controls TTL for stats/control_data
#following parameter allows to specify minimum amount of disk space in the analytics
#database partition, if configured amount of space is not present, it will fail provisioning
#minimum_diskGB = 256

#OPTIONAL BONDING CONFIGURATION
#==============================
#Inferface Bonding
bond= {
    host1 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host2 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host3 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host4 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host5 : { 'name': 'bond0', 'member': ['p6p1', 'p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host6 : { 'name': 'bond0', 'member': ['p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
    host7 : { 'name': 'bond0', 'member': ['p6p2'], 'mode': '802.3ad', 'xmit_hash_policy': 'layer3+4' },
}

#==================================================================================
control_data = {
    host1 : { 'ip': '172.16.80.1/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host2 : { 'ip': '172.16.80.2/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host3 : { 'ip': '172.16.80.3/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host4 : { 'ip': '172.16.80.4/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host5 : { 'ip': '172.16.80.5/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host6 : { 'ip': '172.16.80.6/24', 'gw' : '172.16.80.254', 'device':'bond0' },
    host7 : { 'ip': '172.16.80.7/24', 'gw' : '172.16.80.254', 'device':'bond0' },
}

#OPTIONAL STATIC ROUTE CONFIGURATION  
#===================================  
#storage compute disk config
#storage_node_config = {
#    host4 : { 'disks' : ['/dev/sdc', '/dev/sdd'], 'journal' : ['/dev/sde', '/dev/sdf'] },
#    host5 : { 'disks' : ['/dev/sdc:/dev/sde', '/dev/sdd:/dev/sde'], 'ssd-disks' : ['/dev/sdf', '/dev/sdg'] },
#    host6 : { 'disks' : ['/dev/sdc', '/dev/sdd'], 'local-disks' : ['/dev/sde'], 'local-ssd-disks' : ['/dev/sdf'] },
#    host7 : { 'nfs' : ['10.10.10.10:/nfs', '11.11.11.11:/nfs']},
#}
#
#Set Storage replica
#storage_replica_size = 3

# VIP
env.ha = {
    'internal_vip' : '172.16.80.50',
    'external_vip' : '10.84.29.50'
}

# OPTIONAL vrouter limit parameter
# ==================================

do_parallel = True
env.mail_from='chhandak@juniper.net'
env.mail_to='chhandak@juniper.net'
env.encap_priority =  "'VXLAN','MPLSoUDP','MPLSoGRE'"
env.test_repo_dir='/root/contrail-test'
env.ca_cert_file='/root/cacert.pem'
#env.ca_cert_file='/root/contrail-test/tools/tor/cacert.pem'
