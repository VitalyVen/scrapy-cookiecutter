#!/bin/bash
set -e
cd ..
rm crawler -rf
rm ~/.cookiecutter_replay/scrapy-cookiecutter.json -rf
ls ~/.cookiecutter_replay/scrapy-cookiecutter.json||cookiecutter scrapy-cookiecutter
rm crawler -rf
cookiecutter --replay scrapy-cookiecutter
