################################################################################
#
# env.mk
#
ifdef RNMAKE_DOXY
/*! 
\file 

\brief Aether Instinct rnmake environment override version of the rnmake system
command-line and environment variables helper makefile.

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

export _ENV_MK = 1

# must be defined and non-empty
ifeq ($(AI_WORKSPACE),)
  $(error 'AI_WORKSPACE' environment variable not specified)
endif

# ------------------------------------------------------------------------------
# RNMAKE_ARCH_TAG
# 	What:									Determines which architecture makefile to include.
# 													Arch.$(RNMAKE_ARCH_TAG).mk
# 	Environment variable: AIMAKE_ARCH_DFT
# 	Make override:				make arch=<arch> ...
# 	Default:							x86_64
# 	Required:							no
# ------------------------------------------------------------------------------

# 'make arch=<arch> ...' or AIMAKE_ARCH_DFT or x86_64
AIMAKE_ARCH_DFT ?= x86_64
arch ?= $(AIMAKE_ARCH_DFT)

RNMAKE_ARCH_TAG := $(arch)


# ------------------------------------------------------------------------------
# RNMAKE_INSTALL_XPREFIX
# 	What:									Cross-install prefix.
# 												Actual packages are installed to
# 	                      	$(RNMAKE_INSTALL_XPREFIX)/$(RNMAKE_ARCH)/
# 	Environment variable: AIMAKE_INSTALL_XPREFIX
# 	Make override:				make xprefix=<path> ...
# 	Default:							$(HOME)/xinstall
# 	Required:							no
# ------------------------------------------------------------------------------

# 'make xprefix=<path> ...' or RNMAKE_INSTALL_XPREFIX
AIMAKE_INSTALL_XPREFIX ?= $(HOME)/xinstall
xprefix ?= $(AIMAKE_INSTALL_XPREFIX)

# make cannonical path (does not have to exist)
RNMAKE_INSTALL_XPREFIX := $(abspath $(xprefix))


# ------------------------------------------------------------------------------
# RNMAKE_INSTALL_PREFIX
# 	What:									Install prefix. Overrides RNMAKE_INSTALL_XPREFIX.
# 												Packages are installed to:
# 													$(RNMAKE_INSTALL_PREFIX)/
# 	Environment variable: AIMAKE_INSTALL_PREFIX
# 	Make override:				make prefix=_path_ ...
# 	Default:							
# 	Required:							no
# ------------------------------------------------------------------------------

# 'make prefix=<path> ...' or AIMAKE_INSTALL_PREFIX
prefix ?= $(AIMAKE_INSTALL_PREFIX)

# make cannonical path (does not have to exist)
RNMAKE_INSTALL_PREFIX := $(abspath $(prefix))


# ------------------------------------------------------------------------------
# Export to sub-makes
#
export RNMAKE_ARCH_TAG
export RNMAKE_INSTALL_XPREFIX
export RNMAKE_INSTALL_PREFIX

ifdef RNMAKE_DOXY
/*! \endcond RNMAKE_DOXY */
endif
