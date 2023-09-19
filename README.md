# stadsarkiv-client

## Install for development

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    virtualenv venv # Python >= 3.10.6 should work

    source venv/bin/activate

Install requirements:

    # with pip
    pip install -r requirements.txt

    # or with poetry
    poetry install

### Run for development

Run dev server:

    ./bin/cli.sh server-dev


Show all commands:

    ./bin/cli.sh

### Fix code

Run black, mypy and flake8:

    ./bin/fix.sh

## Install as requirement

Using virtualenv:

    virtualenv venv

    source venv/bin/activate

Install latest version (or upgrade):
<!-- LATEST-VERSION-START -->
	pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@v1.1.24

Uninstall:

    pip uninstall -y stadsarkiv-client

### Run required module

Generate a `./bin/cli.sh` file as shortcut to all module commands:

```bash
#!/bin/sh
./venv/bin/python -m stadsarkiv_client $@
```
    chmod +x bin/cli.sh

For development:

    ./bin/cli.sh server-dev

Start or restart (stop and start) for production (gunicorn):

    ./bin/cli.sh server-prod

Stop server:

    ./bin/cli.sh server-stop

Generate a session secret:

    ./bin/cli.sh server-secret

### Modifying the required module

You may override the default module using the following files and dirs:

    .env
    settings.py
    settings_facets.py
    language.py
    hooks.py
    templates/
    static/

All the above files and dirs are optional. You may see examples of all the above files in the 
[example-config directory](https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/example-config)
(These files are well documented)

These files and dirs should be placed in the directory where you run the module from - otherwise they will be ignored.

## Run on server

[See README.server.md](https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/docs/README.server.md)
