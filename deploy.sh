#!/bin/bash

echo -e "\\033[0;32mDeploying updates to github...\\033[0m"

cleanup() {
  echo -e "\\033[0;32mClean up public directory...\\033[0m"

  # prevent the confirmation question
  setopt localoptions rmstarsilent

  cd public || exit

  git reset --hard
  git checkout master
  # git pull origin master
  rm -rf ./*

  cd ..
}

# Build the site
echo -e "\\033[0;32mBuild site...\\033[0m"

# cleanup 
hugo --i18n-warnings --minify

# Go to public folder
cd public || exit

if [ -n "$GITHUB_AUTH_SECRET" ]
then
    touch ~/.git-credentials
    chmod 0600 ~/.git-credentials
    echo "$GITHUB_AUTH_SECRET" > ~/.git-credentials

    git config credential.helper store
    git config user.email "ingorichter-blog-bot@users.noreply.github.com"
    git config user.name "ingorichter-blog-bot"
fi

# this is no longer necessary, since a CNAME file in static will be copied to the root of the generated site
# recreate the CNAME file
# cat <<CNAMECONTENT >./CNAME
# ingo-richter.io
# CNAMECONTENT

#Add changes to git
# git add -A
git add .

# Commit changes
msg="Rebuild ingo-richter.io $(date "+%Y-%m-%d %H:%M:%S")"
if [ $# -eq 1 ]; then
	msg="$1"
fi
git commit -m "$msg"

# Push source and build repos
# git push --force origin HEAD:master
git push --force "https://${GITHUB_USER}:${GITHUB_PERSONAL_ACCESS_TOKEN}@github.com/ingorichter/ingorichter.github.io" master

# Come back
cd ..
