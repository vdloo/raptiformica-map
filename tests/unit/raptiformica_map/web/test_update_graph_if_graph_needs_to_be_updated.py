from raptiformica_map.update_graph import GRAPH_FILE
from raptiformica_map.web import update_graph_if_graph_needs_to_be_updated
from tests.testcase import TestCase


class TestUpdateGraphIfGraphNeedsToBeUpdated(TestCase):
    def setUp(self):
        self.datetime = self.set_up_patch(
            'raptiformica_map.web.datetime'
        )
        self.datetime.now.return_value = 1
        self.datetime.fromtimestamp.return_value = 2
        self.timedelta = self.set_up_patch(
            'raptiformica_map.web.timedelta'
        )
        self.timedelta.return_value = 0
        self.isfile = self.set_up_patch(
            'raptiformica_map.web.isfile'
        )
        self.getctime = self.set_up_patch(
            'raptiformica_map.web.getctime'
        )
        self.generate_graph = self.set_up_patch(
            'raptiformica_map.web.generate_graph'
        )

    def test_update_graph_if_graph_needs_to_be_updated_gets_now_datetime(self):
        update_graph_if_graph_needs_to_be_updated()

        self.datetime.now.assert_called_once_with()

    def test_update_graph_if_graph_needs_to_be_updated_gets_timedelta(self):
        update_graph_if_graph_needs_to_be_updated()

        self.timedelta.assert_called_once_with(seconds=60)

    def test_update_graph_if_graphs_needs_to_be_updated_checks_if_graph_file_exists(self):
        update_graph_if_graph_needs_to_be_updated()

        self.isfile.assert_called_once_with(GRAPH_FILE)

    def test_update_graph_if_graph_needs_to_be_updated_gets_ctime_from_graph_file(self):
        update_graph_if_graph_needs_to_be_updated()

        self.getctime.assert_called_once_with(GRAPH_FILE)

    def test_update_graph_if_graph_needs_to_be_updated_gets_timestamp_from_ctime(self):
        update_graph_if_graph_needs_to_be_updated()

        self.datetime.fromtimestamp.assert_called_once_with(
            self.getctime.return_value
        )

    def test_update_graph_if_graphs_needs_to_be_updated_updates_graph_if_needs_to_be_updated(self):
        self.isfile.return_value = True
        self.datetime.fromtimestamp.return_value = 1
        self.datetime.now.return_value = 2

        update_graph_if_graph_needs_to_be_updated()

        self.generate_graph.assert_called_once_with()

    def test_update_graph_if_graph_needs_to_be_updated_does_not_update_graph_if_already_updated_just_now(self):
        self.isfile.return_value = True

        update_graph_if_graph_needs_to_be_updated()

        self.assertFalse(self.generate_graph.called)

    def test_update_graph_if_graph_needs_to_be_updated_updates_graph_if_no_graph_file_yet(self):
        self.isfile.return_value = False

        update_graph_if_graph_needs_to_be_updated()

        self.generate_graph.assert_called_once_with()
