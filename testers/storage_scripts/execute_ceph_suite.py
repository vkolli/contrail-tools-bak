#!/usr/bin/python
import subprocess
import sys

testbed = sys.argv[1]
profile = sys.argv[2]

if testbed == "testbed_ceph3.py" :
   tb_file = "SMOKE_CEPH3.config"
else:
   tb_file = "None"

execfile('ceph_profiles.py')


exit_status = 0

for tests in profiles_tests[profile] :
  script_cmd = tests.split(",")
  script_cmd.append(tb_file)
  return_val = subprocess.call(script_cmd)
  exit_status = exit_status or return_val
  
print "CEPH_SANITY suite completed"

sys.exit(exit_status)


