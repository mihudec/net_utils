import unittest
from wildcard_calc import acl_with_wildcard_to_netmasks

class TestWildCardCalc(unittest.TestCase):


    def test_acl_with_wildcard_to_netmasks(self):
        tests = [
            {"source": ["192.168.1.0", "0.0.1.0"], "result": ["192.168.0.0/32", "192.168.1.0/32"]}
        ]
        for test in tests:
            with self.subTest(msg=test):
                result = [x.with_prefixlen for x in acl_with_wildcard_to_netmasks(address_str=test["source"][0], wildcard_str=test["source"][1])]
                self.assertListEqual(result, test["result"])