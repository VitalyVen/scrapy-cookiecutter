# Scrapy-cookiecutter

Powered by [Cookiecutter](https://github.com/audreyr/cookiecutter). scrapy-cookiecutter is a framework for jumpstarting Scrapy projects quickly.

## Introduction
This cookie cutter is boilerplate builder for starting a scrapy project have support sqlachemy (mysql/postrges) pipeline. It comes with basic project structure and configuration.

## Features

- Simple scrapy project with Sqlalchemy pipiline (Postgres/mysql available)
- Docker support using docker-compose for development
- Run tests with pytest
- Default integration with pre-commit for identifying simple issues before submission
- Scrapyd integration
- Integrated crontab task for schedule spiders with scrapyd(option)
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
* other scheduler
* playwright
* pupeeter
* pycharm integration
* all sqlalchemy backends
* pip/poetry
* selenium?
* full settings
* itemadapter

```
#https://docs.scrapy.org/en/latest/topics/coroutines.html#coroutine-support
from itemadapter import ItemAdapter
class DbPipeline:
    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter['field'] = await db.get_some_data(adapter['id'])
        return item
```
