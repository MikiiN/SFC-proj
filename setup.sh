#!/bin/bash

VENV_DIR="venv"      
REQ_FILE="requirements.txt"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$REQ_FILE"
