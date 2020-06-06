################################################################################
#
# The AetherInstinct package top-level makefile.
#
# RN Make System Specific Makefile
#
# @LegalBegin@
# Copyright 2019-2020 Aether Instinct LLC. All Rights Reserved
#
# Licensed under the MIT License (the "License").
#
# You may not use this file except in compliance with the License. You may
# obtain a copy of the License at:
#
#   https://opensource.org/licenses/MIT
#
# The software is provided "AS IS", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. in no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in the
# software.
# @LegalEnd@
# 
################################################################################

#------------------------------------------------------------------------------
# Required

# must be defined and non-empty
ifeq ($(AI_WORKSPACE),)
  $(error 'AI_WORKSPACE' environment variable not specified)
endif

# Package Root Directory
RNMAKE_PKG_ROOT	= $(AI_WORKSPACE)

# Uncomment these two lines if this make file's variables, macros and/or targets
# depend on the make architecture.
#RNMAKE_ARCH_DFT ?= x86_64
#arch ?= $(RNMAKE_ARCH_DFT)

#------------------------------------------------------------------------------
# Subdirectories

RNMAKE_SUBDIRS =  src

#------------------------------------------------------------------------------
# Distribution files

# header files
RNMAKE_HDR_FILES = $(RNMAKE_PKG_ROOT)/src/include/*

# etc files
RNMAKE_ETC_FILES =

# lib configuration files
RNMAKE_LIB_CFG_FILES =

# share files
RNMAKE_SHARE_FILES =

#------------------------------------------------------------------------------
# Extra Targets

.PHONY: update-legal
update-legal:
	@${AI_WORKSPACE}/rnmake/tools/rnupdate_legal \
  	--exclude=share --exlcude=rnmake \
		--verbose \
  	copyright_initial=2019 \
		copyright_holder='Aether Instinct LLC' \
  	license=MIT \
		license_url='https://opensource.org/licenses/MIT' \
  	${AI_WORKSPACE}/pkgcfg/templates/license.tpl

#------------------------------------------------------------------------------
# Include RNMAKE rules makefile(s)

# include top-level rules
include $(RNMAKE_PKG_ROOT)/rnmake/Rules.mk
