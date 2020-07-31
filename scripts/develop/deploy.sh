#!/bin/bash

function isServiceInstalled() {
    echo -e "\e[1;123m*** TEST IF SERVICE IS INSTALLED ON TARGET ***"
    ssh $1 'test -d ~/PirBlaster'
    if [[ $? -ne 0 ]]
    then
        echo -e "\e[1;124mSERVICE NOT INSTALLED ON TARGET"
        exit 1
    fi
    echo -e "\e[1;121mSERVICE INSTALLED ON TARGET"
    return 0
}

function deployNewSrc() {
    echo -e "\e[1;123m*** DEPLOYING NEW SOURCE CODE ***"
    rsync -avz --delete --exclude venv ./ $1:PirBlaster
    if [[ $? -ne 0 ]]
    then
        echo -e "\e[1;124mSOURCE DEPLOYMENT FAILED"
        exit 1
    fi
    echo -e "\e[1;121mNEW SOURCE CODE DEPLOYED"
    return 0
}

function restartService() {
    echo -e "\e[1;123m*** RESTARTING SERVICE ***"
    ssh $1 'sudo systemctl restart pirblaster.service'
    if [[ $? -ne 0 ]]
    then
        echo -e "\e[1;124mSERVICE RESTART FAILED"
        exit 1
    fi
    echo -e "\e[1;121mSERVICE RESTARTED"
    return 0
}

if [[ "$#" -ne 1 ]]
then
    echo -e "\e[1;124mBAD NUMBER OF ARGUMENT!!!"
    exit 1
fi

isServiceInstalled $1
if [[ $? -ne 0 ]]
then
    exit 1
fi

deployNewSrc $1
if [[ $? -ne 0 ]]
then
    exit 1
fi

restartService $1
if [[ $? -ne 0 ]]
then
    exit 1
fi

echo -e "\e[1;121mDEPLOYMENT DONE"
