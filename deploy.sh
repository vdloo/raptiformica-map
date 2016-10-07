#!/bin/bash

# Install bootstrap dependencies on Debian-like machines
if type apt-get > /dev/null 2>&1; then
    apt-get update -y
    apt-get install python3 python-apt python3-dev ansible -y
fi;

# Install bootstrap dependencies on Archlinux machines
if type pacman > /dev/null 2>&1; then
    pacman -Syyu --noconfirm
    pacman -S python3 ansible --noconfirm
fi;

ansible-playbook provisioning/main.yml --connection=local --connection=local -i '127.0.0.1,' -vvv
