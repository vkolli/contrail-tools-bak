#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}

source $TOOLS_WS/testers/utils
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

#get_testbed
exec_cmds -s $TASK_RUNNER_HOST_STRING -p $TASK_RUNNER_HOST_PASSWORD -c "
    cd /tmp/$AVAILABLE_TESTBEDS/;
    git clone git@github.com:Juniper/contrail-tools.git;
    cd contrail-tools/testers/storage_scripts;
    python execute_ceph_suite.py $AVAILABLE_TESTBEDS $PROFILE;
  "
#unlock_testbed $TBFILE_NAME
