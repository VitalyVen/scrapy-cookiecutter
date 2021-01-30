#!/bin/bash
set -e
docker -v
git --version >> /dev/null || sudo apt install git -y
pipenv --version > /dev/null || sudo apt install pipenv -y
pipenv install --dev
pre-commit install
