## setup and build steps

### Python Application
    - Requires python, pip, and pipenv installed before running:
    pipenv shell
    pipenv install
    pipenv run scipy_install
    pipenv install -e .
    python setup.py py2app -d pydist
    exit

### Electron Application
    - Requires node
    npm install
    npm run dist

