#!/bin/sh
pip install -U `pip list --outdated | tail -n +3 | awk '{print $1}'`

