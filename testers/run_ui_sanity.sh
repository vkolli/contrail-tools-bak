#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}

source $TOOLS_WS/testers/utils


function run_ui_sanity {
    if [ $SKIP_SANITY -ne 0 ]
    then
        return 0
    fi
    search_package
    copy_fabric_test_artifacts
    run_fab "setup_test_env"
    run_fab "install_webui_packages:~"
    check_venv_exists
    setup_sanity_base
}

function run_ui_task() {
    get_testbed
    echo "running on testbed $TBFILE_NAME"
    create_testbed || die "Failed to create required testbed details"
    reimage_and_bringup
    #bringup_setup || die "Bringup failed"
    sleep 120
    run_ui_sanity || die "Run_sanity step failed"
    unlock_testbed $TBFILE_NAME
    echo "Test Done" 
    collect_tech_support || die "Task to collect logs/cores failed"
    echo "Ending test on $TBFILE_NAME"
}

run_ui_task 
