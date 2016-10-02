from mock import Mock

from raptiformica_map.web import get_ip
from tests.testcase import TestCase


class TestGetIP(TestCase):
    def setUp(self):
        self.request = self.set_up_patch(
            'raptiformica_map.web.request',
            Mock(headers={'x-real-ip': '1.2.3.4'})
        )

    def test_get_ip_returns_ip_from_header(self):
        ret = get_ip()

        self.assertEqual(ret, '1.2.3.4')

    def test_get_ip_returns_none_if_no_ip_in_header(self):
        self.request.headers = {}

        ret = get_ip()

        self.assertIsNone(ret)
