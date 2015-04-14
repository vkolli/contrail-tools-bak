#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}

source $TOOLS_WS/testers/utils
get_testbed

cd $TOOLS_WS
cd contrail-test/storage_scripts
python execute_ceph_suite.py $AVAILABLE_TESTBEDS $PROFILE
