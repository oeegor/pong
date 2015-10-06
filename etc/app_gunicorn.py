# coding: utf-8
import os

bind = '127.0.0.1:5050'
errorlog = '-'
graceful_timeout = 180
loglevel = 'error'
max_requests = 1000
max_requests_jitter = 1000
timeout = 180
workers = os.environ.get('MOTA_WORKERS_COUNT', 8)
worker_class = os.environ.get('MOTA_WORKER_CLASS', 'eventlet')
worker_connections = os.environ.get('MOTA_WORKER_CONNECTIONS', 300)
