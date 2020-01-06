#!/bin/bash
set -e

# Install bootstrap dependencies on Debian-like machines
if type apt-get > /dev/null 2>&1; then
    apt-get install python3 python-apt python3-dev libffi-dev libssl-dev -y
    apt-get purge ansible -y || /bin/true
    pip install ansible==2.2.3.0
    ansible-playbook provisioning/main.yml --connection=local --connection=local -i '127.0.0.1,' -vvv
fi;

# Install bootstrap dependencies on Archlinux machines
if type pacman > /dev/null 2>&1; then
    # My phone is running a very old kernel and I don't want to go 
    # through the trouble of running a custom one and recompiling,
    # I also don't want to downgrade python2. So instead, manually 
    # running ansible with the python3 interpreter is a good enough
    # workaround for now. 
    # ```
    # [root@android]# python2
    # Python 2.7.13 (default, Apr 24 2017, 20:01:05) 
    # [GCC 6.3.1 20170306] on linux2
    # Type "help", "copyright", "credits" or "license" for more information.
    # >>> import random
    # Traceback (most recent call last):
    #   File "<stdin>", line 1, in <module>
    #   File "/usr/lib/python2.7/random.py", line 885, in <module>
    #     _inst = Random()
    #   File "/usr/lib/python2.7/random.py", line 97, in __init__
    #     self.seed(x)
    #   File "/usr/lib/python2.7/random.py", line 113, in seed
    #     a = long(_hexlify(_urandom(2500)), 16)
    # OSError: [Errno 38] Function not implemented
    # ```
    if ps a | grep -q [c]om.android.phone; then
        pip3 install ansible
        /usr/bin/python3 `which ansible-playbook` provisioning/main.yml \
          --connection=local --connection=local -i '127.0.0.1,' \
          -e 'ansible_python_interpreter=/usr/bin/python3' -vvv
    else
        pacman -S python3 ansible --noconfirm --needed
        # TODO: remove when https://github.com/ansible/ansible/issues/63077 is resolved
        wget -O /usr/lib/python3.8/site-packages/ansible/modules/packaging/os/pacman.py https://raw.githubusercontent.com/ansible/ansible/v2.8.6/lib/ansible/modules/packaging/os/pacman.py
        ansible-playbook provisioning/main.yml \
          --connection=local --connection=local -i '127.0.0.1,' \
          -e 'ansible_python_interpreter=/usr/bin/python3' -vvv
    fi;
fi;

