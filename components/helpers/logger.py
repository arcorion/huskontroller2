import logging
from pathlib import Path

class Logger:
    """
    Logger object that gets used to write to the log file.
    """

    _logger = logging.getLogger('huskontroller')
    _logger.setLevel(logging.DEBUG)

    # Set the log path to the application_root/logs folder.
    _log_path = Path()
    # #####_log_path = _log_path.resolve().parents[1]
    _log_path = _log_path / 'logs'

    # Make sure the log directory exists
    if not _log_path.exists():
        _log_path.mkdir()

    # Set the filehandler output to huskontroller.log
    _file_handler = logging.FileHandler(_log_path + 'huskontroller.log')
    _file_handler.setLevel(logging.DEBUG)

    # Using the format "YYYY-MM-DD HH:MM:SS" for the timestamp, then a
    # dash, and then the actual message.
    _formatter = logging.Formatter(fmt='%(asctime)s - %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
    _file_handler.setFormatter(_formatter)

    # Appl
    _logger.addHandler(_file_handler)
    _logger.info('Logging for touchscreen interface initializing...\n')
    

    
    def __init__(self):
        pass