"""Code for system demos."""


from simple.definitions import DEMO_TEMP_DIR
from simple.logging.log import demo_config_file_log, demo_system_console_log


def demo_logs():
    """Demo for log setup and creation."""
    # Dev Note - all log files should be ignored via vcs
    # Create DEMO_DIR if not yet existing
    DEMO_TEMP_DIR.mkdir(exist_ok=True)
    # Set within package location for demo_temp log files x2
    demo_system_log = DEMO_TEMP_DIR / "demo_system.log"
    demo_config_log = DEMO_TEMP_DIR / "demo_config.log"
    # Run the demo to create console logs
    demo_system_console_log(log_path=demo_system_log)
    # Run the demo to create config file logs
    demo_config_file_log(log_path=demo_config_log)
