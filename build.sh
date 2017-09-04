#!/bin/bash

set -euo pipefail

function debug() {
  case "$1" in
    i*) echo -e  "[$(date)] \e[97m[\e[93minfo\e[97m] $2\e[39m";;
    d*) echo -e  "[$(date)] \e[97m[\e[96mdebug\e[97m] $2\e[39m";;
    w*) echo -e  "[$(date)] \e[97m[\e[91mwarning\e[97m] $2\e[39m";;
    *) exit $?;;
  esac
}

#
# pack as standalone executable binary
#

PYTHON="$(which python)"
debug 'd' "PYTHON => '${PYTHON}'"

export EXECUTABLE='hmdc'
debug 'd' "EXECUTABLE => '${EXECUTABLE}'"

export PATH_SOURCE='hmdc'
export PATH_BUILD='build'
export PATH_OUTPUT="$(pwd)/${PATH_BUILD}/${EXECUTABLE}"
debug 'd' "PATH_SOURCE => '${PATH_SOURCE}'"
debug 'd' "PATH_BUILD => '${PATH_BUILD}'"
debug 'd' "PATH_OUTPUT => '${PATH_OUTPUT}'"

[ -n "$(which zip)" ] && {

  # clean up
  find "${PATH_SOURCE}" -type f -iname '*.py[co]' -delete
  [ -d "${PATH_BUILD}" ] && {
    rm -rfv "${PATH_BUILD}"
    debug 'w' 'previous build already exists => deleting.. OK'
  }
  debug 'i' 'cleaning up.. OK'

  # prepare build
  mkdir -pv "${PATH_BUILD}"
  debug 'i' 'initializing new build path.. OK'

  # pack directories
  (
    cd "${PATH_SOURCE}"
    zip -r "${PATH_OUTPUT}.zip" *
  )
  debug 'i' 'adding source code to stub.. OK'

  # write header
  echo "#!${PYTHON}" > "${PATH_OUTPUT}"
  debug 'i' 'writing header to stub.. OK'

  # write body
  cat "${PATH_OUTPUT}.zip" >> "${PATH_OUTPUT}"
  debug 'i' 'copying stub to executable binary.. OK'

  # permission
  chmod u+x -v "${PATH_OUTPUT}"
  debug 'i' 'setting permission.. OK'

  # clean up
  rm -fv "${PATH_OUTPUT}.zip"
  debug 'i' 'cleaning up.. OK'
}

exit $?
