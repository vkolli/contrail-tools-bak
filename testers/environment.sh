#!/usr/bin/env bash
export TBFILE
export API_SERVER_HOST_STRING=${API_SERVER_HOST_STRING:-"root@127.0.0.1"}
export TOOLS_WS=${TOOLS_WS:-$PWD}

# Set the below 4 variables if PKG_FILE is not set
export BRANCH=${BRANCH:-mainline}
export BUILDID=${BUILDID:-LATEST}
export DISTRO=${DISTRO:-"ubuntu-12-04"}
export SKU=${SKU:-icehouse}

# If BRANCH, BUILID, DISTRO, SKU are not defined,
# PKG_FILE path needs to be set
export PKG_FILE

#--------
# For Tempest
# You can override these from the results of 'fab export_testbed_details' task
export KEYSTONE_SERVICE_HOST=${KEYSTONE_SERVICE_HOST:-127.0.0.1}
export KEYSTONE_SERVICE_HOST_USER=${KEYSTONE_SERVICE_HOST_USER:-root}
export KEYSTONE_SERVICE_HOST_PASSWORD=${KEYSTONE_SERVICE_HOST_PASSWORD:-c0ntrail123}
export API_SERVER_IP=`echo $API_SERVER_HOST_STRING | cut -d @ -f2`
export API_SERVER_HOST_USER=`echo $API_SERVER_HOST_STRING | cut -d @ -f1`
export API_SERVER_HOST_PASSWORD=${API_SERVER_HOST_PASSWORD:-c0ntrail123}
#-------

export SKIP_REIMAGE=${SKIP_REIMAGE:-0}
export SKIP_BRINGUP=${SKIP_BRINGUP:-0}
export SKIP_SANITY=${SKIP_SANITY:-0}

# Skip running tempest by default
export SKIP_TEMPEST=${SKIP_TEMPEST:-1}

# Set NEW_TEST_INFRA to 1 to use the contrail-test code from bhushana/contrail-test
export NEW_TEST_INFRA=${NEW_TEST_INFRA:-0}
export MX_GW_TEST=${MX_GW_TEST:-0}

# By default, new test infra enables parallel run. To force it to run serially  
export SERIAL_RUN=${SERIAL_RUN:-0}

# Knob to add basic images (fab add_basic_images) before the test run
export ADD_IMAGES=${ADD_IMAGES:-0}

# Location can be US or INDIA
# If US, reimage command will be triggered from SVL_HOST_STRING
export TESTBED_LOCATION=${TESTBED_LOCATION:-INDIA}

export SCRIPT_TIMESTAMP=`date +"%Y_%m_%d_%H_%M_%S"`
export SSHOPT="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
export NODEHOME=${NODEHOME:-/root}
export SVL_HOST_STRING=${SVL_HOST_STRING:-stack@10.84.24.64}
export SVL_HOST_PASSWORD=${SVL_HOST_PASSWORD:-c0ntrail123}
export FAB_GIT_BRANCH=${BRANCH:-master}
export PARAMS_FILE=${PARAMS_FILE:-${NODEHOME}/contrail-test/scripts/sanity_params.ini}
export TEST_CONFIG_FILE=${TEST_CONFIG_FILE:-${NODEHOME}/contrail-test/sanity_params.ini}

export BUILD_SCRIPT_PATH=$TOOLS_WS/contrail-test
export FABRIC_SCRIPT_PATH='$TOOLS_WS/contrail-fabric-utils'
export RUN_WITHIN_VENV=0
export EMAIL_SUBJECT=${EMAIL_SUBJECT:-"Sanity Report"}

# Location where locks are maintained for testbeds
export LOCK_FILE_DIR=${LOCK_FILE_DIR:-/cs-shared/test_runs}

if [ ${BRANCH} == "mainline" ]; then
    FAB_GIT_BRANCH='master'
fi

declare -A BUILD_MAP
BUILD_MAP=( [ubuntu-12-04]=ubuntu-12.04.3 [centos64_os]=centos-6.4 [centos65]=centos6.5 [ubuntu-14-04]=ubuntu-14.04)
export REIMAGE_PARAM=${BUILD_MAP[${DISTRO}]}
lsb_dist=''

###########
# For usage outside Juniper, they need to make sure 
# a) fab and test code are copied to cfgm node 
# b) testbed.py should have env.test_repo_dir populated to point to contrail-test code
# c) CFGM_FAB_PATH and CFGM_TEST_CODE_PATH are updated
# d) JUNIPER_INTRANET is set to 0
#
# The default path for fab code is ~/fabric-utils

export CFGM_FAB_PATH=${CFGM_FAB_PATH:-${NODEHOME}/fabric-utils}
export CFGM_TEST_CODE_PATH=${CFGM_TEST_CODE_PATH:-${NODEHOME}/contrail-test}
export JUNIPER_INTRANET=${JUNIPER_INTRANET:-1}

export IMAGE_WEB_SERVER=${IMAGE_WEB_SERVER:-"10.204.216.51"}


