#!/bin/bash

# Install bootstrap dependencies on Debian-like machines
if type apt-get > /dev/null 2>&1; then
    apt-get install python3 python-apt python3-dev -y
    apt-get purge ansible -y
    pip install ansible
    ansible-playbook provisioning/main.yml --connection=local --connection=local -i '127.0.0.1,' -vvv
fi;

# Install bootstrap dependencies on Archlinux machines
if type pacman > /dev/null 2>&1; then
    pacman -S python3 ansible --noconfirm --needed
    /usr/bin/python3 `which ansible-playbook` provisioning/main.yml \
      --connection=local --connection=local -i '127.0.0.1,' \
      -e 'ansible_python_interpreter=/usr/bin/python3' -vvv
fi;

