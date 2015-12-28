# Jenkins sometimes terminates the job even before cleanup is run
LOCK_FILE_DIR=/cs-shared/testbed_locks

echo "Current active jobs: "

(
  flock -n 5
  tb_lock_file=`grep -l "Occupied! .*$BUILD_TAG" $LOCK_FILE_DIR/*.py` || \
                echo "No testbed found for unlocking"
  if [[ ! -s $tb_lock_file ]]; then
    exit 0
  fi
  if ! grep -xq "Testbed locked..Unlock when debug complete" $tb_lock_file ; then
    sed -i "/Occupied! .*$BUILD_TAG/d" $tb_lock_file
  else
    echo "Testbed $tb_lock_file is locked for debug..."
  fi
  cat $tb_lock_file
) 5>${LOCK_FILE_DIR}/lockfile

