# base image
FROM oeegor/baseimage:0.1
ENV HOME=/root
CMD ["/sbin/my_init"]

EXPOSE 80

RUN echo 'v1'

RUN set -xe \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -qq \
    && apt-get upgrade -qq \
    && apt-get install -qqy --no-install-recommends \
        build-essential \
        libpq-dev \
        nginx \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \

    && locale-gen en_US.UTF-8 ru_RU.UTF-8 \

    # we provide our config
    && rm /etc/nginx/nginx.conf \

    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm /var/log/alternatives.log /var/log/apt/history.log /var/log/apt/term.log /var/log/dpkg.log


WORKDIR /opt/app/

COPY requirements.txt /opt/app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY etc/ /etc/

COPY . /opt/app/

RUN set -ex \
    && chmod 644 /etc/logrotate.d/* \
    && find -name '*.pyc' -delete \
    && mkdir -p /var/log/app /var/log/nginx \
    && chmod 644 /etc/cron.d/app \
    && chown -R www-data. /opt/app/ /var/log/app /var/log/nginx \
    && nginx -t \
    && find static -type f -print | sort | xargs cat | md5sum | awk '{ print $1 }' > .media-hash \
    && ./app/manage.py collectstatic --traceback --verbosity=3 --no-input --link
