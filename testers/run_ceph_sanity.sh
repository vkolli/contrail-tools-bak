#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}

source $TOOLS_WS/testers/utils
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

return_val=`exec_cmds -s $TASK_RUNNER_HOST_STRING -p $TASK_RUNNER_HOST_PASSWORD -c "
    cd /tmp/$AVAILABLE_TESTBEDS/;
    rm -rf contrail-tools;
    git clone git@github.com:Juniper/contrail-tools.git;
    cd contrail-tools/testers/storage_scripts;
    python execute_ceph_suite.py $AVAILABLE_TESTBEDS $CEPH_PROFILE;
  "`

flag=`echo $return_val | awk '{print match($0,"CEPH_SANITY_PASS")}'`;
if [ $flag -gt 0 ];then
    die "CEPH_SANITY : FAILED"
else
    echo "CEPH_SANITY : PASS"
fi
