#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}

source $TOOLS_WS/testers/utils
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

get_testbed

cd $TOOLS_WS
cd testers/storage_scripts
python execute_ceph_suite.py $AVAILABLE_TESTBEDS $PROFILE

unlock_testbed $TBFILE_NAME
