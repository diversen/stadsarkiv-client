# README

## Install for dev

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    source venv/bin/activate

Or (Windows)

    source venv/Scripts/activate

    pip install -r requirements.txt

## Run local:

    python -m stadsarkiv_client

Or: 

    ./run-module.sh

## Install as requirement

Update version and install latest version:

    pip uninstall -y stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main 

## Run 

Run with default settings: 

    stadsarkiv-client --port 5000 --reload true

Override settings: 

    touch settings_local.py

```.py
settings_local = {
    "templates_local": "./templates", # Override templates
    "static_local": "./static", # Change static folder
    "static_extra": "./static_extra", # Add extra static folder
    "pages_local": "./pages", # Som default pages in html or md
}
```

Override .env: 

    touch .env

```.env
# session secret
SECRET=SECRET
# developemnt or production
ENVIRONMENT=production
```
