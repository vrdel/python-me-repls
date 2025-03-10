#!/usr/bin/env python

import configparser
import os
import sys
from config import parse_config
from log import Logger

from keystoneauth1.identity import v3
from keystoneclient.v3 import client
from keystoneauth1 import session


logger = Logger('test-keystone-client').get()


class IdentityClient(object):
    def __init__(self, logger, admin_user, admin_password, admin_project,
                 admin_project_id, url, member_role):
        self.logger = logger
        self.admin_user = admin_user
        self.admin_password = admin_password
        self.admin_project = admin_project
        self.admin_project_id = admin_project_id
        self.url = url
        self.member_role = member_role
        self.project_id = None
        self.setup_client()

    def get_role(self, name):
        found = filter(lambda r: r.name == name,
                       self.admin_client.roles.list())
        return found[0] if found else None

    def setup_client(self):
        auth = v3.Password(auth_url=self.url, username=self.admin_user,
                           password=self.admin_password,
                           user_domain_id='default',
                           project_id=self.admin_project_id,
                           project_domain_id='Default',
                           project_name=self.admin_project)
        sess = session.Session(auth=auth)
        self.admin_client = client.Client(session=sess, interface='public')
        self.role = self.get_role(self.member_role)


def main():
    confopts = parse_config()
    keystone = IdentityClient(logger, confopts['openstack']['username'],
                              confopts['openstack']['password'],
                              confopts['openstack']['project_name'],
                              confopts['openstack']['project_id'],
                              confopts['openstack']['url'],
                              confopts['openstack']['member_role'])


if __name__ == '__main__':
    main()
