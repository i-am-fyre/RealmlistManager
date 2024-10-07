import unittest
from unittest.mock import patch, MagicMock
import json
from main import load_config, save_config, update_realmlist, add_configuration

class TestRealmlistUpdater(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"configurations": []}')
    def test_load_config(self, mock_open):
        config = load_config()
        self.assertEqual(config, {'configurations': []})
        mock_open.assert_called_once_with('config.json', 'r')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_config(self, mock_open):
        config_data = {'configurations': [{'name': 'Test Config'}]}
        
        save_config(config_data)
        
        # Verify that the file was opened correctly
        mock_open.assert_called_once_with('config.json', 'w')
        
        # Get the file handle from the mock
        handle = mock_open()
        
        # Check how many times 'write' was called
        self.assertGreaterEqual(handle.write.call_count, 1)  # Should be at least one call

        # Generate the expected output
        expected_output = json.dumps(config_data, indent=4)
        
        # Concatenate all calls to 'write' to create the full output
        actual_written = ''.join(call[0][0] for call in handle.write.call_args_list)
        
        # Check if the actual written output matches the expected output
        self.assertEqual(actual_written.strip(), expected_output.strip())


    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_update_realmlist(self, mock_open):
        realmlist_path = 'realmlist.wtf'
        server_address = 'test.server.address'
        version = 'Vanilla (1.12.x)'

        update_realmlist(realmlist_path, server_address, version)

        mock_open.assert_called_once_with(realmlist_path, 'w')
        mock_open().write.assert_any_call(f'set realmlist {server_address}\n')

    @patch('main.save_config')
    @patch('main.messagebox.showwarning')
    def test_add_configuration_duplicate_name(self, mock_showwarning, mock_save_config):
        config = {'configurations': [{'name': 'Test Config'}]}
        entry_fields = {'name': MagicMock(), 'realmlist': MagicMock(), 'wow_exe': MagicMock(), 'server_address': MagicMock(), 'version': MagicMock()}
        entry_fields['name'].get.return_value = 'Test Config'  # Simulating a duplicate name

        add_configuration(config, entry_fields, None, None, None)

        mock_showwarning.assert_called_once_with("Duplicate Name", "A configuration with this name already exists.")

if __name__ == '__main__':
    unittest.main()
