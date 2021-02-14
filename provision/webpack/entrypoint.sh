#!/bin/bash

cd /app/theme
[ ! -d "node_modules" ] && yarn install --pure-lockfile
exec "$@"