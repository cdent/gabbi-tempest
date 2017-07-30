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
    credentials = []
    service_name = None
    service_type = None

    @classmethod
    def skip_checks(cls):
        service = cls.service_name
        super(GenericGabbiTest, cls).skip_checks()
        if not service:
            # FIXME(cdent): Hack to work around discoverability
            # weirdness
            raise cls.skipException('skipping the base class fake test')
        if not CONF.service_available.get(service):
            raise cls.skipException('%s support is required' % service)

    @classmethod
    def resource_setup(cls):
        super(GenericGabbiTest, cls).resource_setup()
        endpoints, token = cls._get_service_auth([cls.service_type])

        for service_type, url in endpoints.items():
            name = '%s_SERVICE' % service_type.upper()
            os.environ[name] = url

        if cls.service_type in endpoints:
            host = None
            url = endpoints[cls.service_type]
        else:
            host = 'stub'
            url = None

        test_dir = os.path.join(os.path.dirname(__file__), 'gabbits',
                                cls.service_type)
        cls.tests = driver.build_tests(
            test_dir, unittest.TestLoader(), host=host, url=url,
            test_loader_name='tempest.scenario.%s.%s' % (
                cls.__name__, cls.service_type))

        os.environ['SERVICE_TOKEN'] = token

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
    def _get_service_auth(cls, service_types):
        interface = 'public'
        auth = cls.os_admin.auth_provider.get_auth()
        token = auth[0]
        catalog = auth[1]['catalog']

        endpoints = {}
        for service_type in service_types:
            result = jsonhandler.JSONHandler.extract_json_path_value(catalog,
                '$[?type = "%s"].endpoints[?interface = "%s"].url' %
                (service_type, interface))
            endpoints[service_type] = result

        return endpoints, token

    def test_fake(self):
        # NOTE(sileht): A fake test is needed to have the class loaded
        # by the test runner
        pass


class NovaGabbiTest(GenericGabbiTest):
    credentials = ['admin']
    # NOTE(cdent): WTF? 'nova' being the thing in service_available?
    # Boo!
    service_name = 'nova'
    service_type = 'compute'

    @classmethod
    def resource_setup(cls):
        super(NovaGabbiTest, cls).resource_setup()
        # TODO(cdent): not very generic!
        os.environ['IMAGE_REF'] = CONF.compute.image_ref
        os.environ['FLAVOR_REF'] = CONF.compute.flavor_ref


class GlanceGabbiTest(GenericGabbiTest):
    credentials = ['admin']
    service_name = 'glance'
    service_type = 'image'
