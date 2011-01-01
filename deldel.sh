#!/bin/sh
for i in `git status | grep deleted | awk '{print $3}'`; do git rm $i; done
