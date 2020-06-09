#
# Aether Instinct development environment bash shell script.
#
# Sets various environment variables.
#
# source env.sh
#

#echo "${BASH_SOURCE[0]}"

# retreive python3's major.minor version 
_python3_version()
{
  local v
  py=$(which python3)
  if [ -x "${py}" ]
  then
    v=$(${py} --version)
    v=${v#[Pp]ython* }
    v=${v%.[0-9]*}
    echo $v
  else
    echo ''
  fi
}

# paranormal test to see if the component $1 is in the search path $2
_inpath()
{
  local comp
  echo "${2//:/$'\n'}" | while read comp
  do
    if [ "${1}" = "${comp}" ]
    then
      return 0
    fi
  done
  return 1
}

# When this file is sourced, the top of the bash source stack will be this
# file's relative/absolute pathname. Use this to autoset workspace root
# directory.
_root=$(dirname ${BASH_SOURCE[0]})

# workspace root directory path
export AI_WORKSPACE=$(realpath ${_root})

# python 3 major.minor version
export AI_PYTHON_VERSION=$(_python3_version)

# default rnmake architecture.
export AI_ARCH_DFT=x86_64

# development distribution path
_dist=${AI_WORKSPACE}/dist/dist.${AI_ARCH_DFT}

# fix up PATH to include distribution bin
_bindir=${_dist}/bin
if ! _inpath "${_bindir}" "${PATH}"
then
  export PATH=${_bindir}:${PATH}
fi

# fix up LD_LIBRARY_PATH to include distribution libraries
_libdirs="${_dist}/lib ${_dist}/lib/aetherinstinct"
for _d in ${_libdirs}
do
  if ! _inpath "${_d}" "${LD_LIBRARY_PATH}"
  then
    export LD_LIBRARY_PATH=${_d}:${LD_LIBRARY_PATH}
  fi
done

# fix up PYTHONPATH to include distribution python site packages
_pydir=${_dist}/lib/python${AI_PYTHON_VERSION}/site-packages
if ! _inpath "${_pydir}" "${PYTHONPATH}"
then
  export PYTHONPATH=${_pydir}:${PYTHONPATH}
fi

unset _python3_version _inpath _root _dist _bindir _libdirs _pydir _d
