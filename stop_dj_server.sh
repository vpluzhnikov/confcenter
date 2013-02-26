#!/bin/bash
ps -ef | grep manage.py | awk '{print $2}' | xargs -i kill {}
