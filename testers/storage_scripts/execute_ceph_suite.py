#!/usr/bin/python
import commands
print "Executing script : %s"%live_migrate.py
print commands.getoutput('python live_migrate.py live_migrate.conf SMOKE_CEPH3.config')
print "Executed ceph sanity successfully"
