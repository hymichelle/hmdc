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
debug 'd' "\$PYTHON => '${PYTHON}'"

EXECUTABLE='hmdc'
debug 'd' "\$EXECUTABLE => '${EXECUTABLE}'"

PATH_SOURCE='hmdc'
PATH_BUILD='build'
PATH_EXEC="${PATH_BUILD}/${EXECUTABLE}"
debug 'd' "\$PATH_SOURCE => '${PATH_SOURCE}'"
debug 'd' "\$PATH_BUILD => '${PATH_BUILD}'"
debug 'd' "\$PATH_EXEC => '${PATH_EXEC}'"

[ -n "$(which zip)" ] && {

  # create stub
  [ -d "${PATH_BUILD}" ] && {
    rm -rf "${PATH_BUILD}"
    debug 'w' 'previous build already exists => deleting.. OK'
  }

  mkdir -p "${PATH_BUILD}"
  debug 'i' "initializing new build path.. OK"

  zip --quiet -j "${PATH_EXEC}" "${PATH_SOURCE}/__main__.py"
  debug 'i' 'creating new zipped stub.. OK'

  # pack directories
  find "${PATH_SOURCE}" \
       -mindepth 1 \
       -maxdepth 1 \
       -type d \
       -exec zip --quiet -r "${PATH_EXEC}" "{}" \;
  debug 'i' 'adding source code to stub.. OK'

  # write header
  echo "#!${PYTHON}" > "${PATH_EXEC}"
  debug 'i' 'writing header to stub.. OK'

  # write body
  cat "${PATH_EXEC}.zip" >> "${PATH_EXEC}"
  debug 'i' 'copying stub to executable binary.. OK'

  # permission
  chmod a+x "${PATH_EXEC}"
  debug 'i' 'setting permission.. OK'

  # clean up
  rm -f "${PATH_EXEC}.zip"
  debug 'i' 'cleaning up.. OK'
}

exit $?
