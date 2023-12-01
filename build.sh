#!/bin/bash

./venv/bin/python3 -m nuitka main.py --standalone --follow-imports --output-filename=sigmonled
