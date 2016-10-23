from mock import Mock

from raptiformica_map.web import page_send_graph
from tests.testcase import TestCase


class TestPageSendGraph(TestCase):
    def setUp(self):
        self.insert_graph_data = self.set_up_patch(
            'raptiformica_map.web.insert_graph_data'
        )
        self.get_ip = self.set_up_patch(
            'raptiformica_map.web.get_ip'
        )
        self.request = self.set_up_patch(
            'raptiformica_map.web.request',
            Mock(form={'data': 'some_data', 'version': 2})
        )
        self.app = Mock()
        self.set_up_patch('raptiformica_map.web.app', self.app)

    def test_page_send_graph_inserts_graph_data(self):
        page_send_graph()

        self.insert_graph_data.assert_called_once_with(
            ip=self.get_ip.return_value,
            config=self.app.config,
            data=self.request.form['data'],
            version=2
        )

    def test_page_send_graph_assumes_data_version_one_if_no_version_specified(self):
        del self.request.form['version']

        page_send_graph()

        self.insert_graph_data.assert_called_once_with(
            ip=self.get_ip.return_value,
            config=self.app.config,
            data=self.request.form['data'],
            version=1
        )

    def test_page_send_graph_returns_OK_if_no_error(self):
        self.insert_graph_data.return_value = None

        ret = page_send_graph()

        self.assertEqual(ret, 'OK')

    def test_page_send_graph_returns_error_if_error(self):
        self.insert_graph_data.return_value = "some error"

        ret = page_send_graph()

        self.assertEqual(ret, 'Error: some error')
