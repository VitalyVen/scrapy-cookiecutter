FROM python:3.9-slim-buster
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y --no-install-recommends build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev curl\
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && rm -f /var/cache/apt/archives/*.deb

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
COPY ./requirements_dev.txt /requirements_dev.txt


RUN pip install -r /requirements_dev.txt
EXPOSE 6023
