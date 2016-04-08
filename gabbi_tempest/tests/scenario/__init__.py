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
import six.moves.urllib.parse as urlparse
from tempest import config
import tempest.test

CONF = config.CONF


class GenericGabbiTest(tempest.test.BaseTestCase):
    credentials = ['admin']
    # NOTE(cdent): WTF? 'nova' being the thing in service_available?
    # Boo!
    service_name = 'nova'
    service_type = 'compute'

    @classmethod
    def skip_checks(cls):
        service = cls.service_name
        super(GenericGabbiTest, cls).skip_checks()
        if not CONF.service_available.get(service):
            raise cls.skipException('%s support is required' % service)

    @classmethod
    def resource_setup(cls):
        super(GenericGabbiTest, cls).resource_setup()
        url, token = cls._get_service_auth()
        parsed_url = urlparse.urlsplit(url)
        prefix = parsed_url.path.rstrip('/')  # turn it into a prefix
        port = 443 if parsed_url.scheme == 'https' else 80
        host = parsed_url.hostname
        if parsed_url.port:
            port = parsed_url.port

        test_dir = os.path.join(os.path.dirname(__file__), 'gabbits')
        cls.tests = driver.build_tests(
            test_dir, unittest.TestLoader(),
            host=host, port=port, prefix=prefix,
            test_loader_name='tempest.scenario.gabbi')

        os.environ["SERVICE_TOKEN"] = token
        # TODO(cdent): not very generic!
        os.environ['IMAGE_REF'] = CONF.compute.image_ref
        os.environ['FLAVOR_REF'] = CONF.compute.flavor_ref

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
        endpoint_type = 'publicURL'

        auth = cls.os_admin.auth_provider.get_auth()
        endpoints = [e for e in auth[1]['serviceCatalog']
                     if e['type'] == cls.service_type]
        if not endpoints:
            raise Exception("%s endpoint not found" % cls.service_type)
        return endpoints[0]['endpoints'][0][endpoint_type], auth[0]

    def test_fake(self):
        # NOTE(sileht): A fake test is needed to have the class loaded
        # by the test runner
        pass
