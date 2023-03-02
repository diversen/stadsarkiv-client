# README

## Install for development

    git clone https://github.com/aarhusstadsarkiv/stadsarkiv-client.git

    cd stadsarkiv-client

    source venv/bin/activate

Or (Windows)

    source venv/Scripts/activate

    pip install -r requirements.txt

## Run local development

    python -m stadsarkiv_client

Or: 

    ./run-module.sh

## Install as requirement

Update version and install latest version:

    pip uninstall -y stadsarkiv-client
    pip install git+https://github.com/aarhusstadsarkiv/stadsarkiv-client@main 

### Run installed modules

Serve with default settings. This just serves the module with default pages and auth.  

    stadsarkiv-serve

Or using some options:

    stadsarkiv-serve --port 5555 --reload true

### Create .env file

Alter default env:

    touch .env

```.env
# session secret
SECRET=SECRET
# developemnt or production
ENVIRONMENT=production
```

Generate a secret to use in .env:

    stadsarkiv-secret

### Override settings

Override settings: 

    touch settings.py

Example:

https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/settings.py

Or view the module settings:

https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/stadsarkiv_client/settings.py

### Override language

Override language:

    touch language.py

See:
    
https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/language.py

All language string in da:

https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/stadsarkiv_client/locales/da.py

All language string in en:

https://github.com/aarhusstadsarkiv/stadsarkiv-client/blob/main/stadsarkiv_client/locales/en.py

### Ovrerride templates

    mkdir templates

See default templates:

https://github.com/aarhusstadsarkiv/stadsarkiv-client/tree/main/stadsarkiv_client/templates