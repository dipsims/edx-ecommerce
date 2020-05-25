#!/usr/bin/env bash

(cd ecommerce; gunicorn ecommerce.wsgi --user www-data --bind 0.0.0.0:8002 --workers 3) &
nginx -g "daemon off;"