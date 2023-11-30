#!/bin/bash

# Just replace the package in venv
rm -rf ./venv/lib/python3.9/site-packages/tired
cp -r tired ./venv/lib/python3.9/site-packages/tired
