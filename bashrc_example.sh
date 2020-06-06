#
# bashrc_example.sh
#
# Aether Instinct shell script example to be sourced in the .bashrc environment
# during interactive startup.
#
# In this example:
#   + The AI workspace is located at ~/ai.
#   + The native build architecutre is Ubuntu debian 64-bit AMD/Intel. It is
#     the only relevant architecture. That is, no cross-compiling.
#   + The built AI system is installed under the workspace subdirectory devel/.
#

#echo "${BASH_SOURCE[0]}"

# paranormal test to see if a component $1 is in the search path $2
inpath()
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

if [[ -f ~/ai/pkgrc.sh ]]
then
  source ~/ai/pkgrc.sh

  export AIMAKE_ARCH_DFT=x86_64
  export AIMAKE_INSTALL_PREFIX=${AI_WORKSPACE}/devel

  # fix up bash standard paths
  export PATH=${AIMAKE_INSTALL_PREFIX}/bin:${PATH}
  export LD_LIBRARY_PATH=${AIMAKE_INSTALL_PREFIX}/lib:${LD_LIBRARY_PATH}
  export PYTHONPATH=${AIMAKE_INSTALL_PREFIX}/lib/python${AI_PYTHON_VERSION}/site-packages:${PYTHONPATH}

  # fix up bash standard paths
  _d=${AIMAKE_INSTALL_PREFIX}/bin
  if ! inpath ${_d} "${PATH}"
  then
    export PATH=${_d}:${PATH}
  fi

  _d=${AIMAKE_INSTALL_PREFIX}/lib
  if ! inpath ${_d} "${LD_LIBRARY_PATH}"
  then
    export LD_LIBRARY_PATH=${_d}:${LD_LIBRARY_PATH}
  fi

  _d=${AIMAKE_INSTALL_PREFIX}/lib/python${AIMAKE_PYTHON_VERSION}/site-packages
  if ! inpath ${_d} "${PYTHONPATH}"
  then
    export PYTHONPATH=${_d}:${PYTHONPATH}
  fi

  unset _d
fi
