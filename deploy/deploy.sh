#!/bin/bash

ssh mediaCenter 'test -d ~/irblasterbackend || mkdir ~/irblasterbackend'
rsync -avz --exclude='node_modules/' ./ mediaCenter:irblasterbackend
