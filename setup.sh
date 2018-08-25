#!/usr/bin/env bash

set -euo pipefail
venv_d=./venv
if [[ ! -d $venv_d ]]; then
    virtualenv "$venv_d"
fi

pip3 install -r requirements.txt
echo 'Done.'
