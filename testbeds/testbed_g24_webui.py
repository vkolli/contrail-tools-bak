from fabric.api import env

os_username = 'admin'
os_password = 'contrail123'
os_tenant_name = 'demo'
#multi_tenancy = True
webui = True
horizon = False
ui_config = 'contrail'
ui_browser = 'firefox'
host1='root@10.204.217.64'
ext_routers = []
router_asn = 64512
public_vn_rtgt = 10000
public_vn_subnet = "10.84.41.0/24"
host_build = 'stack@10.204.216.49'
env.roledefs = {
    'all': [host1],
    'cfgm': [host1],
    'openstack':[host1],
    'collector': [host1],
    'webui': [host1],
    'control': [host1],
    'compute': [host1],
    'database': [host1],
    'build': [host_build],
}
env.hostnames = {
    'all': ['nodeg24']
}
env.ostypes = {
     host1: 'ubuntu'
}

env.passwords = {
    host1: 'c0ntrail123',
    host_build: 'stack@123',
}
minimum_diskGB=32
env.test_repo_dir='/home/stack/webui_ubuntu_single_node/icehouse/contrail-test'
env.mail_from='pavanap@juniper.net'
env.mail_to='dl-contrail-sw@juniper.net'
env.log_scenario ='Single Node Webui Sanity'

