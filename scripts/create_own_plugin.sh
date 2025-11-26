#!/bin/bash
########################################################################
#
# MODULE:       create_own_plugin.sh
#
# AUTHOR(S):    Anika Weinmann
#               mundialis GmbH & Co. KG, Bonn
#               https://www.mundialis.de
#
# PURPOSE:      This script copies the code from this repo and create a
#               new actinia plugin with the example /helloworld endpoint
#
# SPDX-FileCopyrightText: (c) 2022 by mundialis GmbH & Co. KG
#
# REQUIREMENTS: sudo apt install gitsome # for git support
# USAGE:        Only creating a folder for the new plugin
#                 bash create_own_plugin.sh actinia-ex2-plugin
#               Creating a .git folder for the new plugin
#                 bash create_own_plugin.sh actinia-ex2-plugin git
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
########################################################################

# bash create_own_plugin.sh actinia-tiling-plugin

PLUGIN_NAME=$1
PLUGIN_NAME2=$(tr -s '-' '_' <<< "${PLUGIN_NAME}")


# if [ ! -v "$2" ] && [ "$2" == "git" ]
# then
#   GIT_NAME=""
#   ORG_MSG=""
#   # if [[ -v $3 ]]
#   # then
#   #   GIT_ORGANIZATION=$3
#   #   ORG_MSG=" in the organization ${GIT_ORGANIZATION}"
#   #   GIT_NAME="${GIT_ORGANIZATION}/${PLUGIN_NAME}"
#   # else
#   #   GIT_NAME=${PLUGIN_NAME}
#   # fi
#   echo "GIT repository ${GIT_NAME} will be created${ORG_MSG}"
# else
#   echo "No GIT repository will be created"
# fi


# git clone git@github.com:mundialis/actinia-example-plugin.git
git clone https://github.com/mundialis/actinia-example-plugin.git "${PLUGIN_NAME}"

cd "${PLUGIN_NAME}" || exit

rm -rf .git
rm -f scripts/create_own_plugin.sh

# rename all stings in file from actinia-example-plugin to new PLUGIN_NAME
find . -type f -exec sed -i "s/actinia-example-plugin/${PLUGIN_NAME}/g" {} \;
find . -type f -exec sed -i "s/actinia_example_plugin/${PLUGIN_NAME2}/g" {} \;

# rename file and directory names for new plugin
for file in $(find . -name '*actinia-example-plugin*' | sort --reverse)
do
  DIR=$(dirname "${file}")
  BASENAME=$(basename "${file}")
  new_name=${BASENAME//actinia-example-plugin/$PLUGIN_NAME}
  mv "${file}" "${DIR}"/"${new_name}"
done
for file in $(find . -name '*actinia_example_plugin*' | sort --reverse)
do
  DIR=$(dirname "${file}")
  BASENAME=$(basename "${file}")
  new_name=${BASENAME//actinia_example_plugin/$PLUGIN_NAME2}
  mv "${file}" "${DIR}"/"${new_name}"
done

# create git repo
if [ ! -v "$2" ] && [ "$2" == "git" ]
then
  git init
  git add . && git commit -m "actinia plugin created from https://github.com/actinia-org/actinia-example-plugin"

  echo ""
  echo "Push the code to an empty repo with:"
  echo "cd ${PLUGIN_NAME}"
  echo "git remote add origin <your_git_remote>"
  echo "git push origin main"
fi
