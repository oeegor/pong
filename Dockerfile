# base image
FROM phusion/baseimage:0.9.18
ENV HOME=/root
CMD ["/sbin/my_init"]

EXPOSE 80

RUN echo 'v1'

RUN set -xe \
    # for python 3.5
    && DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:fkrull/deadsnakes \
    && apt-get update -qq \
    && DEBIAN_FRONTEND=noninteractive apt-get upgrade -qq

RUN DEBIAN_FRONTEND=noninteractive apt-get install -qq \
        libpq-dev \
        nginx \
        python3.5 \
        python3.5-dev \
        python3-setuptools \

    && rm /usr/bin/python3 && ln -s /usr/bin/python3.5 /usr/bin/python3 \
    && easy_install3 pip \
    && locale-gen en_US.UTF-8 ru_RU.UTF-8 \

    # we provide our config
    && rm /etc/nginx/nginx.conf \

    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm /var/log/alternatives.log /var/log/apt/history.log /var/log/apt/term.log /var/log/dpkg.log


WORKDIR /opt/app/

COPY requirements.txt /opt/app/
RUN pip3.5 install -r requirements.txt

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
