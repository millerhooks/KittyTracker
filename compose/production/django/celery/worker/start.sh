#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A kittytracker.taskapp worker -l INFO
