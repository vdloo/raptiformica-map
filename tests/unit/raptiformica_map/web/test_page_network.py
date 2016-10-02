from raptiformica_map.web import page_network
from tests.testcase import TestCase


class TestPageNetwork(TestCase):
    def setUp(self):
        self.render_template = self.set_up_patch(
            'raptiformica_map.web.render_template'
        )

    def test_page_network_renders_network_template(self):
        page_network()

        self.render_template.assert_called_once_with(
            'network.html', page='network'
        )

    def test_page_network_returns_rendered_template(self):
        ret = page_network()

        self.assertEqual(ret, self.render_template.return_value)
