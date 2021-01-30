# scrapy-cookiecutter

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter). scrapy-cookiecutter is a framework for jumpstarting Scrapy projects quickly.

## Introduction
This cookie cutter is boilerplate builder for starting a scrapy project have support sqlachemy (mysql/postrges) pipeline. It comes with basic project structure and configuration.

**Features:**

- Simple scrapy project with Sqlalchemy pipiline (Postgres/mysql available)
- Docker-compose
- Scrapyd
- Integrated crontab for schedule spiders (option)
- Integrated celery pipeline (option)
- Use mitmweb for check scraper response or reverse something (optional)
- Debug your spiders by launching main function of spider in Pycharm

## Usage

Step 1: Init project

`cookiecutter https://github.com/VitalyVen/cookiecutter-scrapy.git`

Step 2: Choose options

Step 3: Follow instructions in ReadMe of generated project

## Development


## Roadmap
async reactor
pycharm integration
sqlalchemy backends
pip/pipenv
splash
pupeeter
selenium?
full settings
split scheduler into no/cron/scrapydweb/etc
use_docker

