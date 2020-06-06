#
# Aether Instinct global environment bash shell script.
#
# Sets various environment variables.
#

# retreive python3's major.minor version 
python3_version()
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

# When this file is sourced, the top of the bash source stack will be this
# file's relative/absolute pathname. Use this to autoset workspace root
# directory.
_root=$(dirname ${BASH_SOURCE[0]})

# workspace root directory path
export AI_WORKSPACE=$(realpath ${_root})

# python 3 major.minor version
export AI_PYTHON_VERSION=$(_python3_version)

unset _root
