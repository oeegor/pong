# base image
FROM phusion/baseimage:0.9.17
RUN /etc/my_init.d/00_regen_ssh_host_keys.sh
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
        nodejs \
        npm \
        python-dev \
        python-pip \
        ruby \

    && locale-gen en_US.UTF-8 ru_RU.UTF-8 \

    # we provide our config
    && rm /etc/nginx/nginx.conf \

    # foreman part
    && gem install --no-rdoc --no-ri foreman \

    # cleanup ruby tmp files
    && rm -fr /root/.gem \

    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && rm /var/log/alternatives.log /var/log/apt/history.log /var/log/apt/term.log /var/log/dpkg.log


WORKDIR /var/www/chrn/

COPY Procfile /var/www/chrn/
# run `foreman help export` for docs
RUN foreman export --app=chrn --log=/var/log/chrn --user=www-data --root=/var/www/chrn/ runit /etc/service/

COPY package.json /var/www/chrn/
RUN npm install && rm -fr /root/.npm

RUN mv node_modules _node_modules

COPY requirements.txt /var/www/chrn/
RUN pip install -r requirements.txt --use-wheel

COPY etc/ /etc/

COPY . /var/www/chrn/

RUN set -ex \
    && chmod 644 /etc/logrotate.d/* \
    && find -name '*.pyc' -delete \
    && mkdir -p /var/cache/chrn/multi /var/log/chrn /var/log/nginx \
    && chown -R www-data /var/www/chrn /var/cache/chrn/multi /var/log/chrn /var/log/nginx \
    && nginx -t \
    && mv _node_modules node_modules && nodejs node_modules/gulp/bin/gulp.js production \
    && find static -type f -print | sort | xargs cat | md5sum | awk '{ print $1 }' > .media-hash \
    && ./setup-env-vars.sh django-admin collectstatic --traceback --verbosity=3 --noinput
