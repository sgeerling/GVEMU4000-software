#!/bin/bash
if [ $# -gt 1 ]
then
    rm *~
    rm \#*
    git config --global user.email gopimn@gmail.com
    git config --global user.name gopimn
    git config credential.helper store 
    git add . 
    git commit -m "$*"
    git push
else
    echo "gopimn: Bad ammount of arguments."
    echo "usage: ./gitmyass <commit comment>"
fi

# yeah

