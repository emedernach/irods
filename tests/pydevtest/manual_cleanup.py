#!/usr/bin/env python

import sys
import lib
import configuration

test_user_list = ['alice', 'bobby', 'otherrods']
test_resc_list = ['pydevtest_AnotherResc', 'pydevtest_TestResc']

# make admin session
service_env = lib.get_service_account_environment_file_contents()
admin_name = service_env['irods_user_name']
zone_name = service_env['irods_zone_name']
env_dict = lib.make_environment_dict(admin_name, configuration.ICAT_HOSTNAME, zone_name)
sess = lib.IrodsSession(env_dict, configuration.PREEXISTING_ADMIN_PASSWORD, False)

# remove test stuff
for user_name in test_user_list:
    # get permission on user's collection
    sess.run_icommand('ichmod -rM own {admin_name} /{zone_name}/home/{user_name}'.format(**locals()))
    
    # remove test coll
    res = sess.run_icommand('ils /{zone_name}/home/{user_name}'.format(**locals()))
    try:
        test_coll = res[1].split()[2]
        sess.run_icommand('irm -rf {test_coll}'.format(**locals()))
    except IndexError:
        sys.exc_clear()
    
    # remove user
    sess.run_icommand('iadmin rmuser {user_name}'.format(**locals()))

# remove resources
for resource in test_resc_list:
    sess.run_icommand('iadmin rmresc {resource}'.format(**locals()))
