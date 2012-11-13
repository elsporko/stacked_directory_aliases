#!/bin/bash

#===============================================================================
#
# File:             stacked_alias.sh
#                   
# 
# Description       stacked alias helper functions
#
# Author:           T. Tomaino
# Creation Date:    10/11/2012
#
#===============================================================================

export STACKED_ALIAS=/export/home/ttomaino/scripts/stacked_alias.py

#----------------------------------------------------------------------#
#
# ua() use a stacked alias to change directory, supply alias name ($1)
#
function ua {

    if [ $# -lt 1 ] || [ $# -gt 1 ]; then
        echo "(use-alias) 1 parameter required:  <alias name>"
        return
    fi
    dir=`$STACKED_ALIAS -a $1`
    cd ${dir}
}

#----------------------------------------------------------------------#
#
# ea() echo a stacked alias directory name for use at the command line,
#      supply alias name ($1)
#
function ea {

    if [ $# -lt 1 ] || [ $# -gt 1 ]; then
        echo "(echo-alias) 1 parameter required:  <alias name>"
        return
    fi
    dir=`$STACKED_ALIAS -a $1`
    echo ${dir}
}

#----------------------------------------------------------------------#
#
# da() display the alias file
#
function da {
    echo; $STACKED_ALIAS -d  1; echo
}

#----------------------------------------------------------------------#
#
# aa() add an alias to the alias file, supply alias name ($1) and
#      directory ($2)
#
function aa {
    
    if [ $# -lt 2 ] || [ $# -gt 2 ]; then
        echo "(add-alias) 2 parameters required:  <alias name>  <directory>"
        return
    fi
    alias="$1,$2"

    $STACKED_ALIAS -i $alias
}

#----------------------------------------------------------------------#
#
# ra() remove an alias from the alias file, supply alias name ($1)
#
#
function ra {
    if [ $# -lt 1 ] || [ $# -gt 1 ]; then
        echo "(remove-alias) 1 parameter required:  <alias name>"
    fi
    alias="$1"
    $STACKED_ALIAS -r $alias
}
