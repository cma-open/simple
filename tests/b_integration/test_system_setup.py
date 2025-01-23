"""Tests for the system setup module."""

from simple.definitions import PACKAGE
from simple.setup.system_setup import get_platformdirs, setup_directories


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


def test_log_config():
    """Test for log_config function."""

    # mock out inputs

    # log_config()

    # check files were created
    # check content
    # TODO add test content
    # START HERE >>>>>>>>>>>>>>>>>>>>>>>>>


def test_update_system_log():
    """Test for update_system_log."""


def test_system_setup():
    """Test system setup."""


def test_get_platformdirs(capsys):
    """Test get_platformdirs."""
    # Call get_platformdirs func
    # Note - assume will run on Linux !
    get_platformdirs()
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")

    # Print the captured output for verification
    print("Captured output:")
    for line in output_lines:
        print(line)
    # Assert expectedpath, but note assume system is Linux
    assert (f"/.local/share/{PACKAGE}") in output_lines[0]
    assert (f"/.cache/{PACKAGE}") in output_lines[1]
    assert (f"/.config/{PACKAGE}") in output_lines[2]
    assert (f"/.local/state/{PACKAGE}/log") in output_lines[3]
