#!/bin/bash
SRC=./
TMPDIR=tmp
SUFFIX=.txt
NPROCESS=24

# create temp folder
echo
echo Create temporary directory: $TMPDIR
mkdir $TMPDIR

# start preprocessing
echo Starting preprocessing
python3 preprocessing.py -p $SRC -t $TMPDIR -s $SUFFIX -n $NPROCESS

# concatenate all file to one
echo Merging files
cat $TMPDIR/*$SUFFIX > RedditComments$SUFFIX

# remove all tmp files
echo Remove temporary directory
rm -r $TMPDIR
