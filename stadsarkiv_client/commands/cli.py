"""
File containing CLI commands for the Stadsarkiv Client.
"""

import click
import subprocess
import os
import signal
import secrets
import glob
import sys
import psutil
from stadsarkiv_client import __version__


GUNICORN_PID_FILE = "gunicorn_process.pid"
UVICORN_PID_FILE = "uvicorn_process.pid"


@click.group()
def cli():
    pass


@cli.command(help="Start the production gunicorn server. If running exit and restart.")
@click.option("--port", default=5555, help="Server port.")
@click.option("--workers", default=3, help="Number of workers.")
@click.option("--host", default="0.0.0.0", help="Server host.")
@click.option("-c", "--config-dir", default="local", help="Specify a local config directory.", required=False)
@click.option("--config-dir", default="local", help="Specify a local config directory.", required=False)
def server_prod(port: int, workers: int, host: str, config_dir: str):
    _stop_server(GUNICORN_PID_FILE)

    config_dir = config_dir.rstrip("/\\")
    os.environ["CONFIG_DIR"] = config_dir

    if os.name == "nt":
        print("Gunicorn does not work on Windows. Use server-dev instead.")
        exit(1)

    cmd = [
        # Notice that this can not just be "gunicorn" as it is a new subprocess being started
        "./venv/bin/gunicorn",
        "stadsarkiv_client.app:app",
        f"--workers={workers}",
        f"--bind={host}:{port}",
        "--worker-class=uvicorn.workers.UvicornWorker",
        "--log-level=info",
    ]

    gunicorn_process = subprocess.Popen(cmd)
    _save_pid_to_file(GUNICORN_PID_FILE, gunicorn_process.pid)
    print(f"Started Gunicorn in background with PID: {gunicorn_process.pid}")  # Print the PID for reference


"""
Docker command for starting the production gunicorn server.
Notice: No config-dir option. If needed it should be set in the docker-compose.tml.
Default is 'local'.
"""


@cli.command(help="Start the gunicorn server on docker.")
@click.option("--port", default=5555, help="Server port.")
@click.option("--workers", default=3, help="Number of workers.")
@click.option("--host", default="0.0.0.0", help="Server host.")
def server_docker(port: int, workers: int, host: str):
    cmd = [
        "gunicorn",
        "stadsarkiv_client.app:app",
        f"--workers={workers}",
        f"--bind={host}:{port}",
        "--worker-class=uvicorn.workers.UvicornWorker",
        "--log-level=info",
    ]

    subprocess.call(cmd)


@cli.command(help="Start the running Uvicorn dev-server. Notice: By default it watches for changes in current dir.")
@click.option("--port", default=5555, help="Server port.")
@click.option("--workers", default=1, help="Number of workers.")
@click.option("--host", default="0.0.0.0", help="Server host.")
@click.option("-c", "--config-dir", default="local", help="Specify a local config directory.", required=False)
@click.option("--reload", default=True, help="Reload on changes", required=False)
def server_dev(port: int, workers: int, host: str, config_dir: str, reload=True):
    config_dir = config_dir.rstrip("/\\")
    os.environ["CONFIG_DIR"] = config_dir
    _stop_server(UVICORN_PID_FILE)

    cmd = [
        sys.executable,  # Use the current Python interpreter
        "-m",
        "uvicorn",
        "stadsarkiv_client.app:app",
        f"--port={port}",
        f"--host={host}",
        f"--workers={workers}",
        "--log-level=debug",
    ]

    if reload:
        cmd.append("--reload")

    uvicorn_process = subprocess.Popen(cmd)
    _save_pid_to_file(UVICORN_PID_FILE, uvicorn_process.pid)
    print(f"Started Uvicorn in background with PID: {uvicorn_process.pid}")


@cli.command(help="Stop the running Gunicorn server.")
def server_stop():
    if os.path.exists(GUNICORN_PID_FILE):
        _stop_server(GUNICORN_PID_FILE)
    if os.path.exists(UVICORN_PID_FILE):
        _stop_server(UVICORN_PID_FILE)


@cli.command(help="Generate a session secret.")
@click.option("--length", default=32, help="Length of secret.")
def server_secret(length):
    print(secrets.token_hex(length))


@cli.command(help="Show version.")
def version():
    print(__version__)


def run_tests(config_dir, tests_path_pattern):
    os.environ["TEST"] = "TRUE"
    if config_dir:
        config_dir = config_dir.rstrip("/\\")
        os.environ["CONFIG_DIR"] = config_dir

    print(f"Running tests with config dir: {os.getenv('CONFIG_DIR')}")

    # get test files
    test_files = glob.glob(tests_path_pattern)
    if test_files:
        for test_file in test_files:
            print(f"Running tests in {test_file}")
            subprocess.run(["python", "-m", "unittest", test_file], check=True)
    else:
        print(f"No tests found matching pattern {tests_path_pattern}")


def _allow_dev_commands():
    """
    If running in a virtual environment and if the .is_source file exists,
    then allow dev commands
    """

    if sys.prefix != sys.base_prefix and os.path.exists("stadsarkiv_client/.is_source"):
        return True


if _allow_dev_commands():
    # Only show dev commands if source version
    @cli.command(help="Run all tests.")
    def source_test():
        run_tests(None, "tests/config-default/*.py")
        run_tests("example-config-teater", "tests/config-teater/*.py")
        run_tests("example-config-aarhus", "tests/config-aarhus/*.py")

    @cli.command(help="Fix code according to black, flake8, mypy.")
    def source_fix():
        os.system("black . --config pyproject.toml")
        os.system("mypy  --config-file pyproject.toml .")
        os.system("flake8 . --config .flake8")


def _save_pid_to_file(PID_FILE, pid: int):
    with open(PID_FILE, "w") as file:
        file.write(str(pid))


def _stop_server(pid_file):
    try:
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        # Check if the process exists
        if psutil.pid_exists(pid):
            print(f"Stopping server with PID: {pid}")
            if os.name == "nt":
                os.kill(pid, signal.CTRL_BREAK_EVENT)
            else:
                os.kill(pid, signal.SIGINT)

            print("Server stopped successfully.")
        else:
            print(f"Process with PID {pid} does not exist.")

        if os.path.exists(pid_file):
            print(pid_file)
            os.remove(pid_file)

    except Exception as e:
        print(f"Error stopping the server: {e}")
