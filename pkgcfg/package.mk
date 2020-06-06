################################################################################
#
# pkgcfg/package.mk
#
ifdef RNMAKE_DOXY
/*! 
\file 

\brief The Aether Instinct \h_ai package master makefile.

An rnmake system package specific makefile.

\pkgsynopsis
Aether Instinct

\pkgfile{pkgcfg/package.mk}

\pkgauthor{Robin Knight,robin.knight@roadnarrows.com}

\pkgcopyright{2020,RoadNarrows LLC,http://www.roadnarrows.com}

\license{MIT}

\LegalBegin
 Copyright 2019-2020 Aether Instinct LLC. All Rights Reserved

 Licensed under the MIT License (the "License").

 You may not use this file except in compliance with the License. You may
 obtain a copy of the License at:

   https://opensource.org/licenses/MIT

 The software is provided "AS IS", without warranty of any kind, express or
 implied, including but not limited to the warranties of merchantability,
 fitness for a particular purpose and noninfringement. in no event shall the
 authors or copyright holders be liable for any claim, damages or other
 liability, whether in an action of contract, tort or otherwise, arising from,
 out of or in connection with the software or the use or other dealings in the
 software.
\LegalEnd

\cond RNMAKE_DOXY
 */
endif
#
################################################################################

#$(info DBG: $(lastword $(MAKEFILE_LIST)))

export _PKG_MK = 1

ifndef RNMAKE_PKG_ROOT
  $(error 'RNMAKE_PKG_ROOT' Not defined in including makefile)
endif

#------------------------------------------------------------------------------
# The Package Definition

RNMAKE_PKG 								 = aetherinstinct
RNMAKE_PKG_VERSION_MAJOR   = 0
RNMAKE_PKG_VERSION_MINOR   = 5
RNMAKE_PKG_VERSION_RELEASE = 0
RNMAKE_PKG_VERSION_DATE    = 2019

RNMAKE_PKG_AUTHORS 		= Robin Knight
RNMAKE_PKG_OWNERS			= Aether Instinct LLC
RNMAKE_PKG_URL        = https://github.com/roadnarrows-robotics/aetherinstinct
RNMAKE_PKG_EMAIL      = robin.knight@roadnarrows.com
RNMAKE_PKG_LICENSE    = MIT
RNMAKE_PKG_LOGO       = $(RNMAKE_PKG_ROOT)/docs/images/AILogoWings_48x96.png
RNMAKE_PKG_FAVICON    = $(RNMAKE_PKG_ROOT)/docs/images/favicon.png
RNMAKE_PKG_DESC       = Aether Instinct explorations in artificial intelligence
RNMAKE_PKG_KEYWORDS   = Aether Instinct, neural network, deep learning, artificial intelligetnce
RNMAKE_PKG_DISCLAIMER	= See the LICENSE file for any copyright and licensing information.

# Dotted full version number M.m.r
RNMAKE_PKG_VERSION_DOTTED	= $(RNMAKE_PKG_VERSION_MAJOR).$(RNMAKE_PKG_VERSION_MINOR).$(RNMAKE_PKG_VERSION_RELEASE)

# Concatenated full version number Mmr
RNMAKE_PKG_VERSION_CAT = $(RNMAKE_PKG_VERSION_MAJOR)$(RNMAKE_PKG_VERSION_MINOR)$(RNMAKE_PKG_VERSION_RELEASE)

# Package full name name-M.m.r
RNMAKE_PKG_FULL_NAME = $(RNMAKE_PKG)-$(RNMAKE_PKG_VERSION_DOTTED)

# Package documentation home page template.
# Undefined if no template specified home page.
RNMAKE_PKG_HOME_INDEX =	$(RNMAKE_PKG_ROOT)/pkgcfg/templates/home.html.tpl

#------------------------------------------------------------------------------
# Organization
RNMAKE_ORG 					= Aether Instinct
RNMAKE_ORG_FQ 			= Aether Instinct LLC
RNMAKE_ORG_ABBREV 	= AI
RNMAKE_ORG_URL			= http://AetherInstinct.ai
RNMAKE_ORG_LOGO 	 	= $(RNMAKE_PKG_LOGO)
RNMAKE_ORG_FAVICON 	= $(RNMAKE_PKG_FAVICON)

#------------------------------------------------------------------------------
# Package Optional Variables and Tweaks

# Package Include Directories
RNMAKE_PKG_INCDIRS = $(RNMAKE_PKG_ROOT)/src/include

# Package System Include Directories
RNMAKE_PKG_SYS_INCDIRS =

# Package Library Subdirectories
RNMAKE_PKG_LIB_SUBDIRS	= 

# Link Library Extra Library Directories (exluding local library)
RNMAKE_PKG_LD_LIBDIRS = 

# Release Files (docs)
RNMAKE_PKG_REL_FILES = VERSION.txt README.md INSTALL.md LICENSE

# CPP flags
RNMAKE_PKG_CPPFLAGS	=

# C flags
RNMAKE_PKG_CFLAGS =

# CXX flags
RNMAKE_PKG_CXXFLAGS	=

# Link flags
RNMAKE_PKG_LDFLAGS =

#------------------------------------------------------------------------------
# Package Doxygen Configuration

# Define to build doxygen documention, undefine or empty to disable.
RNMAKE_DOXY_ENABLED := y

# Package doxygen configuration directory.
PKG_DOXY_CONF_DIR = $(RNMAKE_PKG_ROOT)/pkgcfg/doxy

# Package doxygen configuration. Doxygen documentation will not be built
# without this file.
RNMAKE_DOXY_CONF_FILE = $(PKG_DOXY_CONF_DIR)/doxy.conf

# Doxygen field: HTML_HEADER
RNMAKE_DOXY_HTML_HEADER = $(PKG_DOXY_CONF_DIR)/ai_doxy_header.html

# Doxygen field: HTML_FOOT
RNMAKE_DOXY_HTML_FOOTER = $(PKG_DOXY_CONF_DIR)/ai_doxy_footer.html

# HTML_HEADER should <link> to this stylesheet 
RNMAKE_DOXY_HTML_STYLESHEET = $(PKG_DOXY_CONF_DIR)/ai_doxy.css

# All images in this directory are copied to doxygen source image directory
RNMAKE_DOXY_IMAGES = $(RNMAKE_PKG_ROOT)/docs/images

# Doxygen field: PROJECT_LOGO
RNMAKE_DOXY_PROJECT_LOGO = $(RNMAKE_PKG_LOGO)

#------------------------------------------------------------------------------
# Package Pydoc Configuration

# Define to build python documention, undefine or empty to disable.
# RNMAKE_PYTHON_ENABLED must also be defined in Arch.<arch>.mk makefile.
RNMAKE_PYDOC_ENABLED := y

# Pydoc optional index.html template.
# Undefined if no pydoc index page
RNMAKE_PYDOC_INDEX=	$(RNMAKE_PKG_ROOT)/pkgcfg/templates/pydoc.html.tpl

ifdef RNMAKE_DOXY
/*! \endcond RNMAKE_DOXY */
endif
