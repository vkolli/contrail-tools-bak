from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'

host1 = 'root@10.204.216.5'


ext_routers = [('blr-mx2', '10.204.216.245')]
router_asn = 64512
public_vn_rtgt = 19005
public_vn_subnet = "10.204.219.96/29"

host_build = 'ganeshahv@10.204.216.3'

env.roledefs = {
    'all': [host1],
    'cfgm': [host1],
    'control': [host1],
    'compute': [host1],
    'collector': [host1],
    'openstack': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
}

env.hostnames = {
     'all': ['nodeb12']
}

env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'secret',
}
env.ostypes = { 
    host1: 'ubuntu',
    }

env.test_repo_dir='/homes/ganeshahv/git-hub/contrail-test'
#env.test_repo_dir='/homes/ganeshahv/commit_queue/Feb-02/contrail-test'
env.mail_from='ganeshahv@juniper.net'
env.mail_to='ganeshahv@juniper.net'

#To enable haproxy feature
#haproxy = True
