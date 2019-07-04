#!/usr/bin/env sh

# reference:  [[SOLVED] Can i use plugins/git to clone another repo? - General Discussion - Drone](https://discourse.drone.io/t/solved-can-i-use-plugins-git-to-clone-another-repo/1553/6?u=karlredman)
# reference: [Secret in Drone 1.0.0-rc.1 · Issue #130 · appleboy/drone-ssh](https://github.com/appleboy/drone-ssh/issues/130)

# the trick to making this work is to add the ssh_key from the drone cli:
# DRONE_SERVER=$DRONE_SERVER DRONE_TOKEN=$DRONE_TOKEN sudo -E bash -c 'drone secret add --repository ${SSH_USER}/${DRONE_REPO} --name ssh_key --data @.ssh/id_rsa'

set -e

# Configures ssh key based on information from secrets

# only execute the script when secret keys exist
[ -z "$SSH_KEY" ] && echo "missing ssh key" && exit 3
[ -z "$SSH_HOST" ] && echo "missing ssh host" && exit 3
[ -z "$TARGET_REPO" ] && echo "missing target repo" && exit 3

# write the ssh key.
mkdir /root/.ssh
echo -n "$SSH_KEY" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

# add ssh_host to our known hosts.
touch /root/.ssh/known_hosts
chmod 600 /root/.ssh/known_hosts
ssh-keyscan -H $SSH_HOST > /etc/ssh/ssh_known_hosts 2> /dev/null

# reset repo origin -perpetual build...!!!
# git remote remove origin
# git remote add origin git@${SSH_HOST}:${SSH_NAME}/${DRONE_REPO}.git
# git remote -v
# # push to repo
# git push git@$SSH_HOST:${SSH_NAME}/${DRONE_REPO}.git ${BRANCH}

# clone the target
git clone ${TARGET_REPO} /target

# clean the target
rm -rf /target/*

# copy/move data
mv docs/* /target/

# format commit comment from dev repo
message=`git log -1 | sed -n '1p;$p' | sed -e 's/^ *//g'`

# commit and push
cd /target
git add -A
git commit -am "from dev ${message}"
git push origin master
