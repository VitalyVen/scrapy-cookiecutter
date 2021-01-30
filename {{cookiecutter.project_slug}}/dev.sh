#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

echo "Creating dev environment in ./venv_{{cookiecutter.project_slug}}..."
sudo apt-get install libmysqlclient-dev -y

python3 -m venv venv_{{cookiecutter.project_slug}}
source venv_{{cookiecutter.project_slug}}/bin/activate
pip3 install -U pip setuptools
pip3 install -r requirements.txt
source venv_{{cookiecutter.project_slug}}/bin/activate
#TODO: pip3 sync
ls .git/||git init .
pre-commit install

echo ""
echo "  * Created virtualenv environment in ./venv_{{cookiecutter.project_slug}}."
echo "  * Installed all dependencies into the virtualenv."
echo "  * You can now activate the $(python3 --version) virtualenv with this command: \`source venv_{{cookiecutter.project_slug}}/bin/activate\`"
