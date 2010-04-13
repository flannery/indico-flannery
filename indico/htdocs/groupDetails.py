# -*- coding: utf-8 -*-
##
##
## This file is part of CDS Indico.
## Copyright (C) 2002, 2003, 2004, 2005, 2006, 2007 CERN.
##
## CDS Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## CDS Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with CDS Indico; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from MaKaC.common.general import *

from MaKaC.webinterface.rh import groups

if DEVELOPMENT:
    groups = reload(groups)


def index(req, **params):
    return groups.RHGroupDetails( req ).process( params )

def selectMembers(req, **params):
    return groups.RHGroupSelectMembers( req ).process( params )

def addMembers( req, **params ):
    return groups.RHGroupAddMembers( req ).process( params )

def removeMembers( req, **params ):
    return groups.RHGroupRemoveMembers( req ).process( params )

