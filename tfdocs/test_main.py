from tfdocs import main
import pytest
from unittest.mock import patch, MagicMock

@patch('tfdocs.parse_args')
@patch('tfdocs.setup_logs')
@patch('logging.getLogger')
def test_valid_main_call(mock_get_logger, mock_setup_logs, mock_parse_args):
    mock_parser = MagicMock()
    mock_args = {
        "verbose" : 20,
        "serve_logs" : False,
        "func" : MagicMock(name="mock_func"),
        "command" : "test-command"
    }
    mock_parse_args.return_value = (mock_parser, mock_args)
    
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger

    main()
                
    mock_setup_logs.assert_called_once_with(
        print_log_level=20,
        enable_log_streaming=False
    )

    mock_get_logger.assert_called_once_with(__name__.split('.')[0])

    mock_logger.info.assert_called_once_with("Running command test-command")

    mock_args["func"].assert_called_once()

