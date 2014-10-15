#!/bin/bash
#
# This script is meant for running tempest quickly on a Ubuntu machine
# Checkout Juniper tempest code; cd tempest ; Then, 
#
#   'curl -sSL https://raw.githubusercontent.com/Juniper/contrail-tools/testers/tempest/tempest_run.sh | sh'
# or:
#   'wget -qO- https://raw.githubusercontent.com/Juniper/contrail-tools/testers/tempest/tempest_run.sh | sh'
#
# By default, it assumes that openstack, contrail is running on local node
# Target node where Openstack/Contrail is setup can be any node(local/remote)
# If remote, set the below environment variables appropriately

export WORKSPACE=${WORKSPACE:-$(pwd)}
BUILD_STRING_FILE="build_id.txt"
export TEMPEST_DIR=$WORKSPACE
export KEYSTONE_SERVICE_HOST=${KEYSTONE_SERVICE_HOST:-127.0.0.1}

export PUBLIC_NETWORK_NAME=${PUBLIC_NETWORK_NAME:-public_net}
export PUBLIC_NETWORK_SUBNET=${PUBLIC_NETWORK_SUBNET:-10.1.1.0/24}
export PUBLIC_NETWORK_RI_FQ_NAME=${PUBLIC_NETWORK_RI_FQ_NAME:-"default-domain:admin:$PUBLIC_NETWORK_NAME:$PUBLIC_NETWORK_NAME"}
export PUBLIC_NETWORK_RT=${PUBLIC_NETWORK_RT:-10003}
export ROUTER_ASN=${ROUTER_ASN:-64512}
export PUBLIC_ACCESS_AVAILABLE=${PUBLIC_ACCESS_AVAILABLE:-0}

export HTTP_IMAGE_PATH=${HTTP_IMAGE_PATH:-http://10.204.216.51/images/cirros/cirros-0.3.1-x86_64-disk.img}
KEYSTONE_SERVICE_HOST_USER=${KEYSTONE_SERVICE_HOST_USER:-root}
KEYSTONE_SERVICE_HOST_PASSWORD=${KEYSTONE_SERVICE_HOST_PASSWORD:-c0ntrail123}
export TENANT_ISOLATION=${TENANT_ISOLATION:-true}

export API_SERVER_IP=${API_SERVER_IP:-127.0.0.1}
export API_SERVER_HOST_USER=${API_SERVER_HOST_USER:-root}
export API_SERVER_HOST_PASSWORD=${API_SERVER_HOST_PASSWORD:-c0ntrail123}
export OS_USERNAME=${OS_USERNAME:-admin}
export OS_PASSWORD=${OS_PASSWORD:-contrail123}
export OS_TENANT_NAME=${OS_TENANT_NAME:-admin}
export OS_AUTH_URL=http://${KEYSTONE_SERVICE_HOST}:5000/v2.0/
export OS_NO_CACHE=1
export SSHOPT="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

function get_api_server_distro () {
    /usr/bin/sshpass -p $API_SERVER_HOST_PASSWORD ssh $SSHOPT ${API_SERVER_HOST_USER}@${API_SERVER_IP} "if [ -f /etc/lsb-release ]; then (cat /etc/lsb-release | grep DISTRIB_DESCRIPTION | cut -d "=" -f2 )
else
    cat /etc/redhat-release | sed s/\(Final\)//
fi"

}

function command_exists() {
    command -v "$@" > /dev/null 2>&1
}

#Get current Contrail Build version from the node 

build_string_cmd="contrail-version |grep contrail-install |head -1| awk '{print \$2}'"
CONTRAIL_BUILD_STRING=`/usr/bin/sshpass -p $KEYSTONE_SERVICE_HOST_PASSWORD ssh $SSHOPT -t ${KEYSTONE_SERVICE_HOST_USER}@${KEYSTONE_SERVICE_HOST} "$build_string_cmd" 2>/dev/null` || echo "Unable to detect Build Id"

rm -f ${BUILD_STRING_FILE}
echo "Build string is $CONTRAIL_BUILD_STRING"
export CONTRAIL_BUILD_STRING

# API SERVER DISTRO
api_server_distro=`get_api_server_distro` 
echo $api_server_distro $CONTRAIL_BUILD_STRING > ${BUILD_STRING_FILE}

rm -f $WORKSPACE/result*.xml

# Run Tempest tests
if [ -n $PUBLIC_ACCESS_AVAILABLE ];
then
    tests="tempest.api.network.test_networks tempest.api.network.test_routers tempest.api.network.test_ports.PortsTestJSON tempest.api.network.test_ports.PortsTestXML tempest.scenario.test_network_advanced_server_ops tempest.scenario.test_network_basic_ops tempest.api.network.test_security_groups tempest.api.network.test_floating_ips tempest.api.network.test_security_groups_negative tempest.api.network.test_extra_dhcp_options  tempest.api.network.test_networks_negative tempest.api.network.test_routers_negative tempest.api.compute.servers.test_attach_interfaces tempest.api.compute.servers.test_server_metadata tempest.api.compute.servers.test_server_addresses tempest.api.compute.servers.test_server_addresses_negative tempest.api.compute.servers.test_multiple_create tempest.api.network.admin.test_load_balancer_admin_actions tempest.api.network.test_load_balancer"
else
    tests="tempest.api.network.test_networks tempest.api.network.test_routers tempest.api.network.test_ports.PortsTestJSON tempest.api.network.test_ports.PortsTestXML tempest.scenario.test_network_advanced_server_ops tempest.scenario.test_network_basic_ops tempest.api.network.test_security_groups tempest.api.network.test_floating_ips tempest.api.network.test_security_groups_negative tempest.api.network.test_extra_dhcp_options  tempest.api.network.test_networks_negative tempest.api.network.test_routers_negative tempest.api.compute.servers.test_attach_interfaces tempest.api.compute.servers.test_server_metadata tempest.api.compute.servers.test_server_addresses tempest.api.compute.servers.test_server_addresses_negative tempest.api.compute.servers.test_multiple_create tempest.api.network.admin.test_load_balancer_admin_actions tempest.api.network.test_load_balancer"
fi

cd $WORKSPACE 
bash -x $WORKSPACE/run_contrail_tempest.sh -p -V -r $WORKSPACE/result.xml -t -- $tests
