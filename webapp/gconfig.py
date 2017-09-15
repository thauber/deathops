import json
import multiprocessing

bind                = '0.0.0.0:8080'
workers             = 2 #multiprocessing.cpu_count() * 2
accesslog           = '/deathops/log/webapp-access.log'
access_log_format   = '"%({X-Forwarded-For}i)s" %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s'
errorlog            = '-'
worker_class        = 'gevent'
proc_name           = 'webapp'
reload              = True
graceful_timeout    = 30
limit_request_field_size = 0
