#!/bin/bash

s="peat"
cd $s
python3 setup.py
docker-compose run IntOptim bash -c "python main.py" --rm
cd ..
