FROM python:3.9-slim-buster
ENV LANG=C LC_ALL=C PYTHONUNBUFFERED=1
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
COPY ./compose/production/scrapydweb/scrapydweb_settings_v10.py /app/scrapydweb_settings_v10.py
EXPOSE 5000
RUN \
    DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl\
    && pip3 install scrapydweb==1.4.0 \
    && apt-get clean autoclean \
    && apt-get autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/cache/apt/archives/*.deb \
    # Remove temporary files owned by root from the platformtemplate step
    && rm /tmp/* ||true
CMD scrapydweb
