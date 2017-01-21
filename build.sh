#!/bin/bash


REPOS="ras-authentication ras-compose ras-config ras-config-files ras-frontstage ras-gateway ras-registry ras-respondent"
PARENT=`pwd`


# Rebuild .gitignore

if [ -f ".gitignore" ]
then
    rm .gitignore
fi


function clone {

  # Get the repo name and URL:
  name=$1
  repo=$2
  PARENT=`pwd`

  # Make sure we have a non-blank directory name, just in case:
  if [ ! -z "$name" ]
  then

    # Get code

    if [ ! -d "$name" ]
    then
      echo - cloning $repo
      git clone $repo
    else
      echo - Updating $repo
      cd $name
      git pull --rebase
    fi

    # Build up .gitignore

    cd $PARENT
    echo $name >> .gitignore
    #debug: cat .gitignore

  else
    Error: please provide a repository name and a repo URL. $name $repo
    exit 1
  fi

  cd $PARENT
}


# Bulid Java projects

for name in $REPOS
do
  # Make sure we have a non-blank repo name, just in case:
  if [ ! -z "$name" ]
  then

    # Get code

    repo="git@github.com:onsdigital/"${name}".git"
    clone $name $repo

    # Build code

    cd $name
    # NB Configuration information doesn't need a build
    if [ -f "pom.xml" ]
    then
      echo - Maven building $name
      mvn clean package
    elif [ -f "build.gradle" ]
    then
      echo - Gradle building $name
      gradle build
    fi
    cd $PARENT

  fi
done
