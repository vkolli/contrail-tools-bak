#!/usr/bin/python
import sys
import traceback
import os
import re

import ceph
import os_lib
import test_lib
import ostack
import time
import gen_lib

if __name__ == '__main__' :

  try:
    arg = {}
    test_obj = test_lib.lib(arg)
    testbed_config = test_obj.argument['testbed_config']['testbed_config']
    test_conf      = test_obj.argument['test_conf']['test_conf']

    profile_name = test_conf['profile_name']

    fab_node_host = testbed_config['%s,fab_node'%profile_name]
    fab_node = testbed_config['%s,node_name'%fab_node_host]

    fab_node_handle   = test_obj.create_ssh_handle(node_name=fab_node,ntp_update=True)

    ostack.init_credentials(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node])

    cinder_type_list = ostack.get_cinder_type_list(test_obj,fab_node_handle,testbed_config['%s,prompt'%fab_node])
    cinder_type_list.sort()

    config_cinder_type_list = testbed_config['%s,cinder_volume_types'%profile_name][:]
    config_cinder_type_list.sort()

    if cinder_type_list == config_cinder_type_list :
      print "PASS : cinder type-list pass\n"
    else:
      msg =  "ERROR : cinder type-list failed\n"
      print msg
      print "Expected cinder type-list",config_cinder_type_list
      print "Actual cinder type-list",cinder_type_list

      test_obj.argument['err_msg'] += msg


  except SystemExit:
     pass
  except :
    traceback.print_exc()
    test_obj.argument['err_msg'] += "Exception occured"

  test_obj.PostResult()
  test_obj.cleanup()
  if test_obj.argument['err_msg'] == "" :
    sys.exit(0)
  else:
    sys.exit(1)

