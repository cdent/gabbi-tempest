#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import unittest

from gabbi import driver
from gabbi.handlers import jsonhandler
import six.moves.urllib.parse as urlparse
from tempest import config
import tempest.test

CONF = config.CONF

class GenericGabbiTest(tempest.test.BaseTestCase):
    credentials = ['admin']

    @classmethod
    def resource_setup(cls):
        super(GenericGabbiTest, cls).resource_setup()

        cls._set_environ()

        # We support all enabled services, so use base hosts.
        host = 'stub'
        url = None

        fallback_dir = os.path.join(os.getcwd(), 'gabbits')
        gabbi_paths = os.environ.get('GABBI_TEMPEST_PATH', fallback_dir)

        top_suite = unittest.TestSuite()

        for test_dir in gabbi_paths.split(':'):
            dotted_path = test_dir.replace(os.path.sep, '.')
            inner_suite = driver.build_tests(
                    test_dir, unittest.TestLoader(), host=host, url=url,
                    test_loader_name='tempest.scenario%s' % dotted_path)
            top_suite.addTest(inner_suite)

        cls.tests = top_suite

    @classmethod
    def _set_environ(cls):
        # Set test ENVIRON substitutions.
        endpoints, token = cls._get_service_auth()
        for service_type, url in endpoints.items():
            name = '%s_SERVICE' % service_type.upper()
            os.environ[name] = url
            name = '%s_BASE' % service_type.upper()
            os.environ[name] = '://'.join(urlparse.urlparse(url)[0:2])
        os.environ['SERVICE_TOKEN'] = token
        if CONF.compute.image_ref:
            os.environ['IMAGE_REF'] = CONF.compute.image_ref
        if CONF.compute.flavor_ref:
            os.environ['FLAVOR_REF'] = CONF.compute.flavor_ref
        if CONF.compute.flavor_ref_alt:
            os.environ['FLAVOR_REF_ALT'] = CONF.compute.flavor_ref_alt

    @classmethod
    def clear_credentials(cls):
        # FIXME(sileht): We don't want the token to be invalided, but
        # for some obscure reason, clear_credentials is called before/during
        # run. So, make the one used by tearDropClass a dump, and call it
        # manually in run()
        pass

    def run(self, result=None):
        self.setUp()
        try:
            self.tests.run(result)
        finally:
            super(GenericGabbiTest, self).clear_credentials()
            self.tearDown()

    @classmethod
    def _get_service_auth(cls):
        interface = 'public'
        auth = cls.os_admin.auth_provider.get_auth()
        token = auth[0]
        catalog = auth[1]['catalog']

        endpoint_lookup = {}
        for entry in catalog:
            service_type = entry['type']
            endpoints = entry['endpoints']
            for endpoint in endpoints:
                if endpoint['interface'] == interface:
                    endpoint_lookup[service_type] = endpoint['url']

        return endpoint_lookup, token

    def test_fake(self):
        # NOTE(sileht): A fake test is needed to have the class loaded
        # by the test runner
        pass
