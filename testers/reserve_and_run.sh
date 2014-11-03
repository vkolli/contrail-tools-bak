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
        lock_file=$LOCK_FILE_DIR/$tb_filename
        if [[ -s $lock_file ]] 
        then
            echo "Testbed $tb_filename is already occupied"
            continue
        else    
            lock_testbed $tb_filename
            export TBFILE=$i
            trap cleanup EXIT
            run_task $tb_filename
            unlock_testbed $tb_filename
            test_ran=1
            break
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
    
