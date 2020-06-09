#
# bashrc_example.sh
#
# Aether Instinct shell script example to be sourced in the .bashrc environment
# during interactive startup.
#
# In this example:
#   + The AI workspace is located at ~/aetherinstinct.
#   + The native build architecutre is Ubuntu debian 64-bit AMD/Intel. It is
#     the only relevant architecture. That is, no cross-compiling.
#   + The built AI system is installed under the workspace subdirectory devel/.
#

#echo "${BASH_SOURCE[0]}"

# paranormal test to see if a component $1 is in the search path $2
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

if [[ -f ~/aetherinstinct/env.sh ]]
then
  source ~/aetherinstinct/env.sh

  export AI_INSTALL_PREFIX=${AI_WORKSPACE}/devel

  # PATH
  _d=${AI_INSTALL_PREFIX}/bin
  if ! _inpath ${_d} "${PATH}"
  then
    export PATH=${_d}:${PATH}
  fi

  # LD_LIBRARY_PATH
  _d=${AI_INSTALL_PREFIX}/lib/aetherinstinct
  if ! _inpath ${_d} "${LD_LIBRARY_PATH}"
  then
    export LD_LIBRARY_PATH=${_d}:${LD_LIBRARY_PATH}
  fi

  # PYTHONPATH
  _d=${AI_INSTALL_PREFIX}/lib/python${AI_PYTHON_VERSION}/site-packages
  if ! _inpath ${_d} "${PYTHONPATH}"
  then
    export PYTHONPATH=${_d}:${PYTHONPATH}
  fi

  unset _d
fi

unset _inpath
