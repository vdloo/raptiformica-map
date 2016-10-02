from raptiformica_map.web import add_ip
from tests.testcase import TestCase


class TestAddIP(TestCase):
    def setUp(self):
        self.get_ip = self.set_up_patch(
            'raptiformica_map.web.get_ip'
        )
        self.get_ip.return_value = '1.2.3.4'

    def test_add_ip_returns_dict_with_ip(self):
        ret = add_ip()

        self.assertEqual(ret, {'ip': '1.2.3.4'})

