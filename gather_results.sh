#!/bin/bash

#set ssh command
ssh=/usr/bin/ssh
scp=/usr/bin/scp

function remotemkdir {
    $ssh kg291538@students.mimuw.edu.pl "mkdir \$HOME/public_html/TE-model/$1"
}

if [ -z $1 ]; then 
    echo Usage: ./gather_results.sh NEW_DIR_NAME
    #exit
fi 

HOMEDIR=$(ssh kg291538@students.mimuw.edu.pl "echo \$HOME")
DEST=/public_html/TE-model
NEWNAME=$1
PATH=$HOMEDIR$DEST$NEWNAME

cmdmkdir="mkdir "$PATH
echo $cmdmkdir
remotemkdir $NEWNAME

set=1
#for dir in $( /bin/ls | /bin/grep 'batch-run*' | /usr/bin/awk '{print $8}'); do
for dir in $( /bin/ls | /bin/grep 'batch-run*'); do
    # for each directory 

    #get into batch-run-(i)
    cd $dir 

    #create new folder remotely
    remotemkdir $NEWNAME/$set

    # scp all : plots & params file
    $scp *.png kg291538@students.mimuw.edu.pl:~/public_html/TE-model/$NEWNAME/$set
    $scp params.txt kg291538@students.mimuw.edu.pl:~/public_html/TE-model/$NEWNAME/$set

    let set+=1
    cd ..
done
