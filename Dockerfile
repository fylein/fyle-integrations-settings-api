# Pull python base image
FROM python:3.10-slim

# install the requirements from the requirements.txt file via git
RUN apt-get update && apt-get -y install libpq-dev gcc && apt-get install git curl postgresql-client -y --no-install-recommends

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installing requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt && pip install pylint-django==2.3.0

# Copy Project to the container
RUN mkdir -p /fyle-admin-settings
COPY . /fyle-integrations-settings-api/
WORKDIR /fyle-integrations-settings-api

# Do linting checks
#RUN pylint --load-plugins pylint_django --rcfile=.pylintrc **/**.py

#================================================================
# Setup non-root user and permissions
#================================================================
RUN groupadd -r -g 1001 integrations_settings_api_service && \
    useradd -r -g integrations_settings_api_service integrations_settings_api_user && \
    chown -R integrations_settings_api_user:integrations_settings_api_service /fyle-integrations-settings-api

# Switch to non-root user
USER integrations_settings_api_user

# Expose development port
EXPOSE 8000

# Run development server
CMD /bin/bash run.sh
