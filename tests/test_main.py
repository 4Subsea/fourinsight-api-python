from click.testing import CliRunner

from fourinsight.engineroom import __main__ as main


def test_init():
    runner = CliRunner()
    result = runner.invoke(main.init, "testapp")
    assert result.output == "Welcome to the machine, testapp\n"
