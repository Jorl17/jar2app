#!/bin/bash
if [ -z "$1" ]
  then
    PREFIX=/usr/bin
  else
    PREFIX=$1
fi

if [ ! -e  $PREFIX/jar2app_basefiles ]
then
  mkdir $PREFIX/jar2app_basefiles
fi
cp -r jar2app_basefiles/* $PREFIX/jar2app_basefiles
cp jar2app $PREFIX
chmod +x $PREFIX/jar2app

