FROM python:3
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip install pipenv
COPY Pipfile Pipfile.lock /usr/src/app/
RUN pipenv install --system --dev
# COPY ./requirements.txt .

# RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
# RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

# RUN pip install -r requirements.txt
COPY . /usr/src/app/
# RUN python manage.py migrate
# RUN python manage.py collectstatic