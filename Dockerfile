# Pull python base image
FROM python:3.7.4-slim

# install the requirements from the requirements.txt file via git
RUN apt-get update && apt-get -y install libpq-dev gcc && apt-get install git -y --no-install-recommends

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

# Expose development port
EXPOSE 8000

# Run development server
CMD /bin/bash run.sh
