#!/bin/sh

echo "[ ] Sleeping 60s before starting..."
sleep 60
exec "$@"
