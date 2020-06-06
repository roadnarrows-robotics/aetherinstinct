################################################################################
#
# The AetherInstinct src makefile.
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

#------------------------------------------------------------------------------
# Subdirectories 

RNMAKE_SUBDIRS = python scripts

#------------------------------------------------------------------------------
# Include RNMAKE rules makefile(s)

# include top-level rules
include $(RNMAKE_PKG_ROOT)/rnmake/Rules.mk
