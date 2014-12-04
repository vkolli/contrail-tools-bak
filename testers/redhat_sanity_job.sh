#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

get_testbed
create_testbed || die "Failed to create required testbed details"
echo "Running tests on $TBFILE_NAME .."
reimage_setup || debug_and_die "Reimage failed!"
search_third_party_package
run_build_fab "cleanup_repo"
run_build_fab "install_pkg_all:${REDHAT_KERNEL_PACKAGE}"
run_build_fab "setup_rhosp_node"
run_build_fab "update_keystone_admin_token"
run_build_fab "install_pkg_all_without_openstack:${THIRD_PARTY_PKG_FILE}" 

copy_fabric_test_artifacts
run_build_fab "install_pkg_all_without_openstack:${PKG_FILE}"
run_setup_shell_script

run_fab "install_without_openstack" || debug_and_die "Contrail install failed!"
run_fab "update_keystone_admin_token"
#run_fab "setup_interface"
run_fab "setup_without_openstack"  || debug_and_die "Setup failed!"
sleep 120
run_fab "install_test_repo"

run_sanity || die "Run_sanity step failed"
echo "Test Done"
collect_tech_support || die "Task to collect logs/cores failed"
echo "Ending test on $TBFILE_NAME"
unlock_testbed $TBFILE_NAME
