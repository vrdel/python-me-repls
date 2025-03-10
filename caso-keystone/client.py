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
                 member_role):
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
        self.setup_client()

    def get_role(self, name):
        found = filter(lambda r: r.name == name,
                       self.client.roles.list())
        return found[0] if found else None

    def setup_client(self):
        auth = v3.Password(auth_url=self.url, username=self.user,
                           password=self.password,
                           user_domain_id=self.user_domain_id,
                           project_id=self.project_id,
                           project_domain_id=self.project_domain_id,
                           project_name=self.project)
        sess = session.Session(auth=auth)
        self.client = client.Client(session=sess, interface='public')
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
                                  confopts['openstack']['member_role'])

    except exceptions.connection.ConnectFailure as exc:
        logger.error(repr(exc))
    except Exception as exc:
        logger.error(f'{exc.url}({exc.method}) {repr(exc)}')


if __name__ == '__main__':
    main()
