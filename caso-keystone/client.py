#!/usr/bin/env python

import configparser
import os
import sys
from config import parse_config
from log import Logger

from keystoneauth1.identity import v3
from keystoneclient.v3 import client
from keystoneauth1 import session
from keystoneauth1 import exceptions


logger = Logger('test-keystone-client').get()


class IdentityClient(object):
    def __init__(self, logger, user, password, project,
                 project_id, project_domain_id, user_domain_id, url,
                 member_role, interface, system_scope):
        self.logger = logger
        self.user = user
        self.password = password
        self.project = project
        self.project_id = project_id
        self.url = url
        self.member_role = member_role
        self.project_id = None
        self.project_domain_id = project_domain_id
        self.user_domain_id = user_domain_id
        self.interface = interface
        self.system_scope = system_scope
        self.setup_client()

    def get_role(self, name):
        found = list(filter(lambda r: r.name == name,
                            self.client.roles.list()))
        return found[0] if found else None

    def setup_client(self):
        auth = v3.Password(auth_url=self.url, username=self.user,
                           password=self.password,
                           user_domain_id=self.user_domain_id,
                           project_id=self.project_id,
                           project_domain_id=self.project_domain_id,
                           project_name=self.project,
                           system_scope=self.system_scope)
        sess = session.Session(auth=auth)
        self.client = client.Client(session=sess, interface=self.interface)
        token = sess.get_token()
        logger.info("Authenticated")
        logger.info(f"Authentication token: {token}")
        self.role = self.get_role(self.member_role)


def main():
    confopts = parse_config()
    try:
        keystone = IdentityClient(logger, confopts['openstack']['username'],
                                  confopts['openstack']['password'],
                                  confopts['openstack']['project_name'],
                                  confopts['openstack']['project_id'],
                                  confopts['openstack']['project_domain_id'],
                                  confopts['openstack']['user_domain_id'],
                                  confopts['openstack']['url'],
                                  confopts['openstack']['member_role'],
                                  confopts['openstack']['interface'],
                                  confopts['openstack']['system_scope'])

    except Exception as exc:
        if getattr(exc, 'url', None) and getattr(exc, 'method', None):
            logger.error(f'{exc.url}({exc.method}) {repr(exc)}')
        else:
            logger.error(repr(exc))


if __name__ == '__main__':
    main()
