#!/usr/bin/python
import commands
commands.getoutput('python live_migrate.py live_migrate.conf SMOKE_CEPH3.config')
print "Executed ceph sanity successfully"
