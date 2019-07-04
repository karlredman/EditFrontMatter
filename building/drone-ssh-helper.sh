#!/usr/bin/env sh


# fail on error
set -e

# Configures ssh key based on information from secrets

# only execute the script when github token exists.
[ -z "$SSH_KEY" ] && echo "Secret Error: missing ssh key" && exit 3
[ -z "$SSH_HOST" ] && echo "Secret Error: missing ssh host" && exit 3
#
[ -z "$USER_EMAIL" ] && echo "Secret Error: missing user email" && exit 3
[ -z "$USER_NAME" ] && echo "Secret Error: missing user name" && exit 3


# write the ssh key.
mkdir /root/.ssh
echo -n "$SSH_KEY" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

# add github.com to our known hosts.
touch /root/.ssh/known_hosts
chmod 600 /root/.ssh/known_hosts
ssh-keyscan -H $SSH_HOST > /etc/ssh/ssh_known_hosts 2> /dev/null

if [ "$1" = "submodule" ]; then
    git config --global user.email "${USER_EMAIL}"
    git config --global user.name "${USER_NAME}"
    # get submodules checkout
    git submodule update --init --recursive
    cd site
    git checkout gh-pages
    # paranoia
    git pull origin gh-pages
    cd ..
    # clean files for build
    rm -rf site/*
elif [ "$1" = "commit" ]; then
    git config --global user.email "${USER_EMAIL}"
    git config --global user.name "${USER_NAME}"
    # get commit specs from master
    MSG=$(git log --pretty=oneline --abbrev-commit -1)
    cd site
    git add -A
    git commit -am "drone build from master: (${MSG})"
    git push origin HEAD:gh-pages
else
    echo "drone-helper.sh Error: function not specified"
    exit 3
fi
