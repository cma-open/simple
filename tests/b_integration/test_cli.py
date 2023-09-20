"""Integration tests for the cli tool."""

#  Simple implementation of integration tests (cf. unit tests)
#  Testing multiple components in an application to ensure that they work as
#  expected when integrated together.


from simple.cli import cli_entry_point


def test_cli_entry_point(capsys):
    """Test cli entry point function (for tool CLI-SIMPLE)."""
    # Set user inputs
    argv = ["2", "2"]
    # Run function with user inputs
    output = cli_entry_point(argv=argv)
    # Expect function to return none
    assert output is None
    # Check stdout output
    captured = capsys.readouterr()
    # Expect that function will have printed result to stdout
    expected = "['4.000005', '4.000005']\n"
    # Assert expected output in the captured.out
    assert captured.out == expected


# TODO
# how is integration test different to end to end test for cli tools?
