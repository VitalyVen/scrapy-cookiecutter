FROM python:3.9-slim-buster
ENV LANG=C LC_ALL=C PYTHONUNBUFFERED=1
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
COPY ./compose/production/scrapyd/scrapyd.conf /etc/scrapyd/
COPY ./requirements.txt /requirements.txt
{%- if cookiecutter.scheduler == 'cron' %}
COPY ./compose/production/scrapyd/cronjob.sh /cronjob.sh
{%- endif %}
RUN \
    DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl git \
    {%- if cookiecutter.scheduler == 'cron' %}
    cron nano\
    {%- endif %}
    && apt-get clean autoclean \
    && apt-get autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/cache/apt/archives/*.deb \
    # Remove temporary files owned by root from the platformtemplate step
    && rm /tmp/* ||true
COPY . .
RUN mkdir -p /var/lib/scrapyd/logs
RUN pip3 install -r /requirements.txt
COPY . .
RUN pip3 install ./compose/production/scrapyd/async_scrapyd/
RUN scrapyd& scrapyd-deploy localhost && rm -f twistd.pid
CMD ["sh", "-c", "logparser -dir /var/lib/scrapyd/logs & scrapyd"]
#TODO: warning: multiple processes in one docker
