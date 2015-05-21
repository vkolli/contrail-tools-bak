#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}
source $TOOLS_WS/testers/utils
source $TOOLS_WS/testers/utils_ceph
source $TOOLS_WS/testers/smgr_utils
source $TOOLS_WS/testers/smgr_utils_ceph
# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

get_testbed
run_smgr_task_ceph
run_ceph_sanity.sh
unlock_testbed $TBFILE_NAME
