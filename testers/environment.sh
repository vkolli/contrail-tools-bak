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
export SKIP_ZONES=${SKIP_ZONES:-0}
export SKIP_SANITY=${SKIP_SANITY:-0}
export SKIP_LOGS_COLLECTION=${SKIP_LOGS_COLLECTION:-0}
# Skip running tempest by default
export SKIP_TEMPEST=${SKIP_TEMPEST:-1}
export SKIP_SM_PROVISION=${SKIP_SM_PROVISION:-0}

# Enable tests which depend on public network connectivity
export MX_GW_TEST=${MX_GW_TEST:-0}

# By default, new test infra enables serial run. To force it to run in parallel 
export PARALLEL_RUN=${PARALLEL_RUN:-0}

# Knob to add basic images (fab add_basic_images) before the test run
export ADD_IMAGES=${ADD_IMAGES:-0}

# Location can be REMOTE or LOCAL 
# If REMOTE, reimage command will be triggered from TASK_RUNNER_HOST_STRING
export TESTBED_LOCATION=${TESTBED_LOCATION:-"LOCAL"}

export SCRIPT_TIMESTAMP=`date +"%Y_%m_%d_%H_%M_%S"`
export SSHOPT="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "
export NODEHOME=${NODEHOME:-/root}
export FAB_GIT_BRANCH=${BRANCH:-master}
export PARAMS_FILE=${PARAMS_FILE:-${NODEHOME}/contrail-test/scripts/sanity_params.ini}
export TEST_CONFIG_FILE=${TEST_CONFIG_FILE:-${NODEHOME}/contrail-test/sanity_params.ini}

export BUILD_SCRIPT_PATH=$TOOLS_WS/contrail-test
export FABRIC_SCRIPT_PATH='$TOOLS_WS/contrail-fabric-utils'
export RUN_WITHIN_VENV=0
export EMAIL_SUBJECT_PREFIX=${EMAIL_SUBJECT_PREFIX:-""}

# Location where locks are maintained for testbeds
export LOCK_FILE_DIR=${LOCK_FILE_DIR:-/cs-shared/testbed_locks}

# Folder where debug logs/cores etc. are put
export DEBUG_LOG_DIR=${DEBUG_LOG_DIR:-/cs-shared/test_runs}

if [ ${BRANCH} == "mainline" ]; then
    FAB_GIT_BRANCH='master'
fi

declare -A BUILD_MAP
BUILD_MAP=( [ubuntu-12-04]=ubuntu-12.04.3 [centos64_os]=centos-6.4 [centos65]=centos-6.5 [ubuntu-14-04]=ubuntu-14.04 [redhat70]=redhat-7.0)
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

# Choose whether to release the testbed on completion or not
# Default is to release
export RELEASE_TESTBED=${RELEASE_TESTBED:-1}

# Set test type to be one of daily/regression.
# Used by contrail-test/tools/upload_to_webserver.py
export TEST_TYPE=${TEST_TYPE:-daily}

# Incase reimage/bringup fails, locks the testbed for debugging 
# if the below variable is set. Default behavior is not to lock
export LOCK_TESTBED_ON_FAILURE=${LOCK_TESTBED_ON_FAILURE:-0}

# Kernel package for setting up Redhat nodes
export REDHAT_KERNEL_PACKAGE=${REDHAT_KERNEL_PACKAGE:-"/cs-shared/builder/cache/redhatenterpriselinuxserver70/icehouse/kernel-3.10.0-123.el7.0contrail.x86_64.rpm"}

# Choose whether to use the task-runner node for running fab cmds
# Typically used when we want to invoke tasks locally on a remote testbed
export USE_TASK_RUNNER_HOST=${USE_TASK_RUNNER_HOST:-0}
export TASK_RUNNER_HOST_STRING=${TASK_RUNNER_HOST_STRING:-stack@10.84.24.64}
export TASK_RUNNER_HOST_PASSWORD=${TASK_RUNNER_HOST_PASSWORD:-c0ntrail123}

# Set this flag if you need to pick latest contrail-test code instead of 
# the contrail-test artifact from the build
# Default is to pick test code from build-artifacts path
export USE_LATEST_TEST_CODE=${USE_LATEST_TEST_CODE:-0}
