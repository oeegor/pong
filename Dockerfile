# base image
FROM phusion/baseimage:0.9.17
ENV HOME=/root
CMD ["/sbin/my_init"]

# our project build commands
EXPOSE 80

RUN set -xe \
    && apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qq \
        libpq-dev \
        nginx \
        python-dev \
        python-pip \

    && locale-gen en_US.UTF-8 ru_RU.UTF-8 \

    # we provide our config
    && rm /etc/nginx/nginx.conf \

    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm /var/log/alternatives.log /var/log/apt/history.log /var/log/apt/term.log /var/log/dpkg.log


WORKDIR /opt/app/

RUN pip install pip --upgrade
COPY requirements.txt /opt/app/
RUN pip install -r requirements.txt --use-wheel

COPY etc/ /etc/

COPY . /opt/app/

RUN set -ex \
    && chmod 644 /etc/logrotate.d/* \
    && find -name '*.pyc' -delete \
    && mkdir -p /var/log/app /var/log/nginx \
    && chown -R www-data. /opt/app/ /var/log/app /var/log/nginx \
    && nginx -t \
    && find static -type f -print | sort | xargs cat | md5sum | awk '{ print $1 }' > .media-hash \
    && ./app/manage.py collectstatic --traceback --verbosity=3 --noinput
