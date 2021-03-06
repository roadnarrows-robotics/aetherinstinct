################################################################################
#
# ./sw/pyModules/src/Makefile
#
ifdef RNMAKE_DOXY
/*!
\file

\brief The \h_laelaps python modules source makefile.

RN Make System Specific Makefile

\pkgsynopsis
RoadNarrows Robotics \h_laelaps Small Mobile Robot Package

\pkgfile{sw/pyModules/src/Makefile}

\pkgauthor{Robin Knight,robin.knight@roadnarrows.com} 

\pkgcopyright{2016-2018,RoadNarrows LLC,http://www.roadnarrows.com}

\license{MIT}

\EulaBegin
\EulaEnd

 * \cond RNMAKE_DOXY
 */
endif
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
# Extras
#

EXTRA_TGT_ALL 	= all-extmod
EXTRA_TGT_CLEAN	= clean-extmod

SWIG_FILES 				= # WatchDogMsgs.i RoboClawMsgs.i ImuMspMsgs.i
SWIG_EXTMOD_DIR 	= # ../modules/Laelaps
SWIG_EXTMOD_LIBS 	= # -llaelaps -lrnr

all-extmod: swig-all

# Clean extension module intermediates
clean-extmod: swig-clean


#------------------------------------------------------------------------------
# Include RNMAKE rules makefile(s)

# include top-level rules
include $(RNMAKE_PKG_ROOT)/rnmake/Rules.mk

# include swig rules
include $(RNMAKE_PKG_ROOT)/rnmake/Rules.swig.mk


ifdef RNMAKE_DOXY
/*! \endcond RNMAKE_DOXY */
endif
