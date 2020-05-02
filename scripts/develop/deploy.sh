#!/bin/bash

ssh labPi 'test -d ~/PirBlasterBackend || mkdir ~/PirBlasterBackend'
rsync -avz ./ labPi:PirBlasterBackend
