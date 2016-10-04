#!/bin/bash
ansible-playbook provisioning/main.yml --connection=local --connection=local -i '127.0.0.1,' -vvv
