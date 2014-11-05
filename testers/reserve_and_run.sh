#!/usr/bin/env bash

TOOLS_WS=${TOOLS_WS:-$(pwd)}

source $TOOLS_WS/testers/utils

# AVAILABLE_TESTBEDS is a comma separated list of testbed filenames or paths
testbeds=(${AVAILABLE_TESTBEDS//,/ })
echo "AVAILABLE TESTBEDS : ${testbeds[@]}"

test_ran=0
while :
do
    for i in "${testbeds[@]}"
    do
        tb_filename=`basename $i`
        if lock_testbed $tb_filename ; then
            trap cleanup EXIT
            export TBFILE=$i
            export TBFILE_NAME=`basename $TBFILE`
            echo "Locked testbed $tb_filename"
            run_task $tb_filename
            unlock_testbed $tb_filename
            test_ran=1
            break
        else
            echo "Testbed $tb_filename is not yet available"
            continue
        fi
    done
    if [[ $test_ran -eq 1 ]]
    then
        echo "Test done"
        break
    fi
    echo "Waiting for testbeds..retrying in 60 sec"
    sleep 60
done
    
