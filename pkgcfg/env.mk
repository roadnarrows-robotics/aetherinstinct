################################################################################
#
ifdef RNMAKE_DOXY
/*! 
\file 

\brief Aether Instinct rnmake environment overrides.

\pkgsynopsis
RN Make System, AI version.

\pkgfile{pkgcfg/env.mk}

\pkgauthor{Robin Knight,robin.knight@roadnarrows.com}

\pkgcopyright{2020,RoadNarrows LLC,http://www.roadnarrows.com}

\license{MIT}

\EulaBegin
\EulaEnd

\cond RNMAKE_DOXY
 */
endif
#
################################################################################

#$(info DBG: $(lastword $(MAKEFILE_LIST)))

export _PKGCFG_ENV_MK = 1

# must be defined and non-empty
ifeq ($(AI_WORKSPACE),)
  $(error 'AI_WORKSPACE' environment variable not specified)
endif

# ------------------------------------------------------------------------------
# RNMAKE_ARCH_DFT
#   Determines default architecture to make.
#
#   Environment variable: AI_ARCH_DFT
#   Fallback default:     x86_64
# ------------------------------------------------------------------------------

# 'make arch=<arch> ...' or @ID_PKG@_ARCH_DFT or x86_64
AI_ARCH_DFT ?= x86_64

# rnmake variable
RNMAKE_ARCH_TAG = $(AI_ARCH_DFT)

# ------------------------------------------------------------------------------
# RNMAKE_INSTALL_XPREFIX
#   Cross-install prefix. Actual packages are installed to:
#   $(RNMAKE_INSTALL_XPREFIX)/$(RNMAKE_ARCH)/
#
#   Environment variable: AI_INSTALL_XPREFIX
#   Fallback default:     $(HOME)/xinstall
# ------------------------------------------------------------------------------

# 'make xprefix=<path> ...' or RNMAKE_INSTALL_XPREFIX
AI_INSTALL_XPREFIX ?= $(HOME)/xinstall

# rnmake variable
RNMAKE_INSTALL_XPREFIX = $(AI_INSTALL_XPREFIX)

# ------------------------------------------------------------------------------
# RNMAKE_INSTALL_PREFIX
#   Install prefix. Overrides RNMAKE_INSTALL_XPREFIX. Packages are installed to:
#   $(RNMAKE_INSTALL_PREFIX)/
#
#   Environment Variable: AI_INSTALL_PREFIX
# ------------------------------------------------------------------------------

# rnmake variable
RNMAKE_INSTALL_PREFIX = $(AI_INSTALL_PREFIX)

# ------------------------------------------------------------------------------
# Export to sub-makes
#
export RNMAKE_ARCH_DFT
export RNMAKE_INSTALL_XPREFIX
export RNMAKE_INSTALL_PREFIX

ifdef RNMAKE_DOXY
/*! \endcond RNMAKE_DOXY */
endif
