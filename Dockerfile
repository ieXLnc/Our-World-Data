FROM python:3

# set working dir
WORKDIR /dash_app

# copy and install requirement
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy app folder to app folder in container
COPY . /dash_app

# chaning to non root user
# Changing to non-root user
RUN useradd -m dash_appUser
USER dash_appUser

# use port var of heroku
CMD gunicorn --bind 0.0.0.0:$PORT app:server