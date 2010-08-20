# -*- coding: utf-8 -*-
##
## $Id: actions.py,v 1.8 2009/04/25 13:56:04 dmartinc Exp $
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
"""
from MaKaC.plugins.base import ActionBase
from MaKaC.plugins.Collaboration.WebEx.common import EVOControlledException, getEVOAnswer, EVOException,\
    getEVOOptionValueByName
from MaKaC.i18n import _

pluginActions = [
    ("reloadCommunityList", {"buttonText": _("Reload Community List"),
                            "associatedOption": "communityList"} )
]

class ReloadCommunityListAction(ActionBase):
    
    def call(self):

        try:
            answer = getEVOAnswer("reloadCommunityList")
        except EVOControlledException, e:
            raise EVOException('Error when parsing list of communities. Message from EVO Server: "' + e.message + '".')
        
        try:
            communityStringList = answer.split('&&')
            communities = {}
            
            ignoredCommunities = getWebExOptionValueByName("ingnoredCommunities")
            
            for communityString in communityStringList:
                id, name = communityString.split(',')
                id = id.strip()
                name = name.strip()
                if id not in ignoredCommunities:
                    communities[id] = name
            self._plugin.getOption("communityList").setValue(communities)
            
        except Exception, e:
            raise EVOException('Error when parsing list of communities. Message from EVO Server: "' + answer + '". Exception ocurred: ' + str(e))
            

"""                 
