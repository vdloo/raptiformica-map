from raptiformica_map.graph_plotter import strip_leading_zeroes
from tests.testcase import TestCase


class TestStripLeadingZeroes(TestCase):
    def test_strip_leading_zeroes_returns_complete_string_if_no_zeroes(self):
        no_leading_zeroes_ipv6 = 'fc14:7b25:b1d5:d9ea:be0f:7a48:4e91:52f9'

        ret = strip_leading_zeroes(no_leading_zeroes_ipv6)

        self.assertEquals(ret, no_leading_zeroes_ipv6)

    def test_strip_leading_zeroes_returns_string_with_stripped_zeroes_after_colons(self):
        leading_zeroes_after_colons_ipv6 = 'fc14:7b25:01d5:d9ea:0e0f:7a48:4e91:52f9'

        ret = strip_leading_zeroes(leading_zeroes_after_colons_ipv6)

        self.assertEquals(ret, 'fc14:7b25:1d5:d9ea:e0f:7a48:4e91:52f9')

    def test_strip_leading_zeroes_returns_string_with_stripped_zeroes_from_beginning(self):
        leading_zeroes_after_beginning_ipv6 = '0c14:7b25:b1d5:d9ea:be0f:7a48:4e91:52f9'

        ret = strip_leading_zeroes(leading_zeroes_after_beginning_ipv6)

        self.assertEquals(ret, 'c14:7b25:b1d5:d9ea:be0f:7a48:4e91:52f9')
