{{cookiecutter.project_name}} {{ '=' * cookiecutter.project_name|length }}

{{cookiecutter.description}}

.. image:: https://img.shields.io/badge/built%20with-Scrapy%20Cookiecutter-b4ff69.svg?logo=cookiecutter
     :target: https://github.com/VitalyVen/scrapy-cookiecutter
     :alt: Built with Cookiecutter Scrapy
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

{% set is_open_source = cookiecutter.license != 'Not open source' -%}
{% if is_open_source %}
* Free software: {{ cookiecutter.license }}
{% endif %}

Basic Commands
--------------

Install project dependencies (optional, if you develop without docker)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    $ ./dev.sh

Start containers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    $ docker-compose up

Run spider by Crawl process (allow to debug as well)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    $ docker-compose run -w /app/{{cookiecutter.project_slug}}/spiders/ scrapy python3 spider.py


Deploy spider to scrapyd container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    $ docker-compose run -w /app/ scrapy scrapyd-deploy

Schedule one task with scrapyd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    $ docker-compose run scrapy curl http://scrapyd:6800/schedule.json -d project={{cookiecutter.project_slug}} -d spider=spider{% if cookiecutter.scheduler=='cron' %}

    Note: if you add requirements after build, it should not be installed because of https://github.com/scrapy/scrapyd/issues/246, rebuild scrapyd image first

Schedule task with cron
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    $ docker-compose run scrapyd bash /cronjob.sh

Edit cron task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    $ docker-compose run scrapyd crontab -e{% endif %}{% if cookiecutter.scheduler=='scrapydweb' %}

Open scrapydweb web page to schedule your spider (do not forget deploy spider first)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    $ xdg-open http://localhost:5005{% endif %}
