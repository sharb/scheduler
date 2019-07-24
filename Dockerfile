FROM python:3 as dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FROM python:3.7.2-stretch as prod

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# CMD ["uwsgi", "app.ini"]

# FROM alpine:3.7 as prod
# # EXPOSE 3031
# # VOLUME /usr/src/app/public
# WORKDIR /usr/src/app
# RUN apk add --no-cache \
#         uwsgi-python3 \
#         python3
# COPY --from=dev /usr/src/app /usr/src/app
# # RUN rm -rf public/*
# RUN pip3 install --no-cache-dir -r requirements.txt
# CMD [ "uwsgi", "--socket", "0.0.0.0:80", \
#                "--uid", "uwsgi", \
#                "--plugins", "python3", \
#                "--protocol", "uwsgi", \
# #                "--wsgi", "main.py" ]

# FROM nginx as nginx

# RUN rm /etc/nginx/conf.d/default.conf

# COPY nginx.conf /etc/nginx/conf.d/