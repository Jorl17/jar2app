#!/bin/bash
if [ -z "$1" ]
  then
    PREFIX=/usr/bin
  else
    PREFIX=$1
fi

rm -rf $PREFIX/jar2app_basefiles
rm -f $PREFIX/jar2app
