import unittest

from mock import patch
from util import Response
import netaddr

import pynetbox


api = pynetbox.api(
    "http://localhost:8000",
    version='2.0'
)

nb = api.ipam

HEADERS = {
    'accept': 'application/json; version=2.0;'
}


class GenericTest(object):
    name = None
    name_singular = None
    ret = pynetbox.lib.response.IPRecord
    app = 'ipam'
    ip_obj_fields = {}

    def test_get_all(self):
        with patch(
            'pynetbox.lib.query.requests.get',
            return_value=Response(fixture='{}/{}.json'.format(
                self.app,
                self.name
            ))
        ) as mock:
            ret = getattr(nb, self.name).all()
            self.assertTrue(ret)
            self.assertTrue(isinstance(ret, list))
            self.assertTrue(isinstance(ret[0], self.ret))
            mock.assert_called_with(
                'http://localhost:8000/api/{}/{}/'.format(
                    self.app,
                    self.name.replace('_', '-')
                ),
                headers=HEADERS
            )

    def test_filter(self):
        with patch(
            'pynetbox.lib.query.requests.get',
            return_value=Response(fixture='{}/{}.json'.format(
                self.app,
                self.name
            ))
        ) as mock:
            ret = getattr(nb, self.name).filter(pk=1)
            self.assertTrue(ret)
            self.assertTrue(isinstance(ret, list))
            self.assertTrue(isinstance(ret[0], self.ret))
            mock.assert_called_with(
                'http://localhost:8000/api/{}/{}/?pk=1'.format(
                    self.app,
                    self.name.replace('_', '-')
                ),
                headers=HEADERS
            )

    def test_get(self):
        with patch(
            'pynetbox.lib.query.requests.get',
            return_value=Response(fixture='{}/{}.json'.format(
                self.app,
                self.name_singular or self.name[:-1]
            ))
        ) as mock:
            ret = getattr(nb, self.name).get(1)
            self.assertTrue(ret)
            self.assertTrue(isinstance(ret, self.ret))
            self.assertTrue(isinstance(dict(ret), dict))
            self.assertTrue(isinstance(str(ret), str))
            mock.assert_called_with(
                'http://localhost:8000/api/{}/{}/1/'.format(
                    self.app,
                    self.name.replace('_', '-')
                ),
                headers=HEADERS
            )
            if self.ip_obj_fields:
                for field in self.ip_obj_fields:
                    self.assertTrue(
                        isinstance(getattr(ret, field), netaddr.IPNetwork)
                    )
                    self.assertTrue(netaddr.IPNetwork(dict(ret)[field]))


class PrefixTestCase(unittest.TestCase, GenericTest):
    name = 'prefixes'
    name_singular = 'prefix'
    ip_obj_fields = ['prefix']


class IPAddressTestCase(unittest.TestCase, GenericTest):
    name = 'ip_addresses'
    name_singular = 'ip_address'
    ip_obj_fields = ['address']


class RoleTestCase(unittest.TestCase, GenericTest):
    name = 'roles'


class RIRTestCase(unittest.TestCase, GenericTest):
    name = 'rirs'


class AggregatesTestCase(unittest.TestCase, GenericTest):
    name = 'aggregates'
    ip_obj_fields = ['prefix']


class VlanTestCase(unittest.TestCase, GenericTest):
    name = 'vlans'


class VlanGroupsTestCase(unittest.TestCase, GenericTest):
    name = 'vlan_groups'


class VRFTestCase(unittest.TestCase, GenericTest):
    name = 'vrfs'


# class ServicesTestCase(unittest.TestCase, GenericTest):
#     name = 'services'
