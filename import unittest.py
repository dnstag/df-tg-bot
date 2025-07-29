import unittest
from unittest.mock import patch, MagicMock, call
import sys
import io
from df_tg_bot import parse_argv, add_help_text, start, help_texts, VERSION

class TestDFTGBot(unittest.TestCase):
    
    def setUp(self):
        """Reset help_texts before each test"""
        help_texts.clear()
    
    def test_parse_argv_minimal_args(self):
        """Test parse_argv with minimal required arguments"""
        test_args = ['test_token']
        with patch.object(sys, 'argv', ['df-tg-bot.py'] + test_args):
            args = parse_argv()
            self.assertEqual(args.token, 'test_token')
            self.assertEqual(args.config, 'config.json')
            self.assertFalse(args.development)
    
    def test_parse_argv_all_args(self):
        """Test parse_argv with all arguments"""
        test_args = ['-c', 'custom_config.json', '-d', 'test_token']
        with patch.object(sys, 'argv', ['df-tg-bot.py'] + test_args):
            args = parse_argv()
            self.assertEqual(args.token, 'test_token')
            self.assertEqual(args.config, 'custom_config.json')
            self.assertTrue(args.development)
    
    def test_parse_argv_version(self):
        """Test parse_argv version flag"""
        test_args = ['-v']
        with patch.object(sys, 'argv', ['df-tg-bot.py'] + test_args):
            with self.assertRaises(SystemExit):
                parse_argv()
    
    def test_add_help_text(self):
        """Test add_help_text function"""
        add_help_text('test', 'Test command description')
        self.assertIn('/test - Test command description', help_texts)
        
        add_help_text('another', 'Another test command')
        self.assertEqual(len(help_texts), 2)
        self.assertIn('/another - Another test command', help_texts)
    
    @patch('df_tg_bot.DLBOTA')
    @patch('df_tg_bot.POTA')
    @patch('df_tg_bot.Config')
    @patch('df_tg_bot.ApplicationBuilder')
    @patch('df_tg_bot.logger')
    def test_start_development_mode(self, mock_logger, mock_app_builder, mock_config, mock_pota, mock_dlbota):
        """Test start function in development mode"""
        # Setup mocks
        mock_app = MagicMock()
        mock_app_builder.return_value.token.return_value.build.return_value = mock_app
        mock_cfg = MagicMock()
        mock_config.return_value = mock_cfg
        
        # Call function
        start('test_config.json', 'test_token', True)
        
        # Verify calls
        mock_config.assert_called_once_with('test_config.json')
        mock_app_builder.assert_called_once()
        mock_app_builder.return_value.token.assert_called_once_with('test_token')
        mock_pota.assert_called_once_with(mock_app, add_help_text, mock_cfg)
        mock_dlbota.assert_called_once_with(mock_app, add_help_text)
        mock_app.run_polling.assert_called_once()
        mock_app.run_webhook.assert_not_called()
    
    @patch('df_tg_bot.DLBOTA')
    @patch('df_tg_bot.POTA')
    @patch('df_tg_bot.Config')
    @patch('df_tg_bot.ApplicationBuilder')
    @patch('df_tg_bot.logger')
    def test_start_production_mode(self, mock_logger, mock_app_builder, mock_config, mock_pota, mock_dlbota):
        """Test start function in production mode"""
        # Setup mocks
        mock_app = MagicMock()
        mock_app_builder.return_value.token.return_value.build.return_value = mock_app
        mock_cfg = MagicMock()
        mock_cfg.webhook_url = 'https://example.com/webhook'
        mock_config.return_value = mock_cfg
        
        # Call function
        start('test_config.json', 'test_token', False)
        
        # Verify calls
        mock_config.assert_called_once_with('test_config.json')
        mock_app_builder.assert_called_once()
        mock_app_builder.return_value.token.assert_called_once_with('test_token')
        mock_pota.assert_called_once_with(mock_app, add_help_text, mock_cfg)
        mock_dlbota.assert_called_once_with(mock_app, add_help_text)
        mock_app.run_polling.assert_not_called()
        mock_app.run_webhook.assert_called_once_with(
            listen="0.0.0.0",
            port=10000,
            webhook_url='https://example.com/webhook'
        )
    
    @patch('df_tg_bot.DLBOTA')
    @patch('df_tg_bot.POTA')
    @patch('df_tg_bot.Config')
    @patch('df_tg_bot.ApplicationBuilder')
    @patch('df_tg_bot.logger')
    def test_start_command_handlers_added(self, mock_logger, mock_app_builder, mock_config, mock_pota, mock_dlbota):
        """Test that help and start command handlers are added"""
        # Setup mocks
        mock_app = MagicMock()
        mock_app_builder.return_value.token.return_value.build.return_value = mock_app
        mock_cfg = MagicMock()
        mock_config.return_value = mock_cfg
        
        # Call function
        start('test_config.json', 'test_token', True)
        
        # Verify command handlers were added
        self.assertEqual(mock_app.add_handler.call_count, 2)
        # Check that CommandHandler was called for help and start commands
        handler_calls = mock_app.add_handler.call_args_list
        self.assertEqual(len(handler_calls), 2)

if __name__ == '__main__':
    unittest.main()