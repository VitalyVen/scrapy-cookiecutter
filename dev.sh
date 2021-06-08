#!/bin/bash
set -e
docker -v || echo "install docker to use it"
git --version >> /dev/null || sudo apt install git -y
poetry --version > /dev/null || "install poetry first with pip3 install poetry"
poetry install
pre-commit install
