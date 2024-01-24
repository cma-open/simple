"""Tests for the system setup module."""


from simple.setup.system_setup import setup_directories

# log_config, setup_system_log

# Mock out paths normally set in config
# Patch out functions at the location used, not where defined
# @patch("simple.setup.system_setup.return_demo_temp")  # Note the source!
# @patch("simple.setup.system_setup.return_logs_dir")  # Note the source!
# @patch("simple.setup.system_setup.return_scratch")  # Note the source!
# @patch("simple.setup.system_setup.return_outputs")  # Note the source!
# @patch("simple.setup.system_setup.return_inputs")  # Note the source!
# def test_key_directories(
#     mock_inputs, mock_outputs, mock_scratch, mock_logs, tmp_path
# ):
#     """Test setup of system directories."""
#     # Set the return value for mocked functions
#     # These wil all be Path objects
#     mock_inputs.return_value = tmp_path / "inputs"
#     mock_outputs.return_value = tmp_path / "outputs"
#     mock_scratch.return_value = PosixPath('/home/example/user/temp/scratch')
#     mock_logs.return_value = PosixPath('/home/example/user/temp/logs')
#     mock_logs.return_value = PosixPath('/home/example/user/temp/logs')
#     setup_directories(datadir_root_path=tmp_pat)
#     assert (tmp_path / "inputs").is_dir()
#     assert (tmp_path / "outputs").is_dir()
#     assert (tmp_path / "scratch").is_dir()
#     assert (tmp_path / "logs").is_dir()


# Test create required subdirectories
def test_setup_directories(tmp_path):
    """Test setup of system directories."""
    # These wil all be Path objects
    key_directories = [
        tmp_path / "inputs",
        tmp_path / "outputs",
        tmp_path / "scratch",
        tmp_path / "logs",
        tmp_path / "demo_temp",
    ]
    setup_directories(key_directories=key_directories)
    assert (tmp_path / "inputs").is_dir()
    assert (tmp_path / "outputs").is_dir()
    assert (tmp_path / "scratch").is_dir()
    assert (tmp_path / "logs").is_dir()
    assert (tmp_path / "demo_temp").is_dir()


# # Test via creating dirs into tmp_path
# # Mock out the main return_datadir root dir with tmp_path
# @patch("simple.config.reader.return_datadir")
# def test_setup_directories(mock_datadir, tmp_path):
#     """Test setup_directories based on configfile."""
#     mock_datadir.return_value = tmp_path
#     with patch("simple.config.reader.configfile", TEST_CONFIGFILE):
#         # Create dirs, as specified by config file
#         setup_directories(datadir_root_path=tmp_path)
#         # Check expected files exist in the main root/data directory
#         expected_data_dirs = ["test_inputs", "test_outputs", "test_scratch"]
#         for subdir in expected_data_dirs:
#             subdir_path = tmp_path / "data" / subdir
#             assert subdir_path.is_dir()
#         # Check the logs dir has been created at root/logs
#         expected_logs_dir = "test_logs"
#         assert (tmp_path / expected_logs_dir).is_dir()
#


def test_log_config():
    """Test for log_config function."""

    # mock out inputs

    # log_config()

    # check files were created
    # check content
    # TODO add test content
    # START HERE >>>>>>>>>>>>>>>>>>>>>>>>>


def test_setup_system_log():
    """Test for setup_system_log."""
    # setup_system_log()
    # needs thought here
    # does this work?
    # or move setup_system_log to init?
    # however its difficult because it has to read from config to work ?
    # check init


def test_update_system_log():
    """Test for update_system_log."""


def test_system_setup():
    """Test system setup."""
