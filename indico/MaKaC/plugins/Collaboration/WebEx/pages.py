# -*- coding: utf-8 -*-
##
## $Id: pages.py,v 1.9 2009/04/25 13:56:04 dmartinc Exp $
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

from MaKaC.plugins.Collaboration.base import WCSPageTemplateBase, WJSBase
from MaKaC.webinterface.pages.collaboration import WAdvancedTabBase
from MaKaC.common.utils import formatDateTime
from MaKaC.webinterface.common.tools import strip_ml_tags, unescape_html
from MaKaC.plugins.Collaboration.WebEx.common import getMinStartDate,\
    getMaxEndDate
from MaKaC.i18n import _
import re

class WNewBookingForm(WCSPageTemplateBase):

    def getVars(self):
        vars = WCSPageTemplateBase.getVars( self )
        vars["EventTitle"] = self._conf.getTitle()
        vars["EventDescription"] = unescape_html(strip_ml_tags( self._conf.getDescription())).strip()

        vars["DefaultStartDate"] = formatDateTime(self._conf.getAdjustedStartDate())
        vars["DefaultEndDate"] = formatDateTime(self._conf.getAdjustedEndDate())

        vars["DefaultWebExUser"] = ""
        vars["DefaultWebExPass"] = ""
        vars["TimeZone"] = self._conf.getTimezone()
        sessions = "<select name='session' id='session' onchange='updateSessionTimes()'><option value=''>None</option>"
        count = 0
        sessionList = self._conf.getSessionList()
        for session  in sessionList:
            count = count + 1
            sessions = sessions + "<option value='%s'>%s</option>" % (str(session.getId()), session.getTitle() )
        sessions += "</select>"
        vars["SessionList"] = sessions

        return vars

class WAdvancedTab(WAdvancedTabBase):

    def getVars(self):
        variables = WAdvancedTabBase.getVars(self)
#        if booking.showAccessPassword():
#            variables["showAccessPassword"] = "yes"
#        else:
#            variables["showAccessPassword"] = "no"
        return variables

class WMain (WJSBase):

    def getVars(self):
        vars = WJSBase.getVars( self )

        vars["AllowedStartMinutes"] = self._WebExOptions["allowedPastMinutes"].getValue()
        vars["MinStartDate"] = formatDateTime(getMinStartDate(self._conf))
        vars["MaxEndDate"] = formatDateTime(getMaxEndDate(self._conf))
        vars["AllowedMarginMinutes"] = self._WebExOptions["allowedMinutes"].getValue()
#        from MaKaC.common.logger import Logger
        vars["LoggedInEmail"] = self._user.getEmail()
#        Logger.get('WebEx').error(self._user.getEmail())
        return vars

class WExtra (WJSBase):

    def getVars(self):
        vars = WJSBase.getVars( self )
        vars["SessionTimes"] = "{}"
        vars["MinStartDate"] = ''
        vars["MaxEndDate"] = ''
        vars["AllowedStartMinutes"] = self._WebExOptions["allowedPastMinutes"].getValue()
        vars["LoggedInEmail"] = self._user.getEmail()
        sessionTimes = ""
        if not hasattr(self, "_conf") or self._conf == None:
            return vars
        sessionList = self._conf.getSessionList()
        for session  in sessionList:
            sessionTimes = sessionTimes + """{"id":"%s", "start":"%s", "end":"%s" },""" % (str(session.getId()), formatDateTime(session.getAdjustedStartDate()), formatDateTime(session.getAdjustedEndDate()) )
        vars["SessionTimes"] = '{ "sessions": [' + sessionTimes[:-1] + ']}'
        if self._conf:
            vars["MinStartDate"] = formatDateTime(getMinStartDate(self._conf), format = "%a %d/%m %H:%M")
            vars["MaxEndDate"] = formatDateTime(getMaxEndDate(self._conf), format = "%a %d/%m %H:%M")
        return vars

class WIndexing(WJSBase):
    pass

class WInformationDisplay(WCSPageTemplateBase):

    def __init__(self, booking, displayTz):
        WCSPageTemplateBase.__init__(self, booking.getConference(), 'WebEx', None)
        self._booking = booking
        self._displayTz = displayTz

    def getVars(self):
        vars = WCSPageTemplateBase.getVars( self )
        vars["Booking"] = self._booking
        return vars

class XMLGenerator(object):
    @classmethod
    def getFirstLineInfo(cls, booking, displayTz):
         return booking._bookingParams["meetingTitle"]
    @classmethod
    def getDisplayName(cls):
        return "WebEx"

    @classmethod
    def getCustomBookingXML(cls, booking, displayTz, out):
#        from MaKaC.common.logger import Logger
#        from MaKaC.user import AvatarHolder
#        for av in AvatarHolder().
#        Logger.get('WebEx').error(booking._conf.getCreator().getEmail())
        booking.checkCanStart()
        params = booking.getBookingParams()
        if (booking.canBeStarted()):
            out.openTag("launchInfo")
            out.writeTag("launchText", _("Join Now!"))
            out.writeTag("launchLink", booking.getUrl())
            out.writeTag("launchTooltip", _('Click here to join the WebEx meeting!'))
            out.closeTag("launchInfo")
        out.openTag("information")
        out.openTag("section")
        out.writeTag("title", _('Title:'))
        out.writeTag("line", params["meetingTitle"])
        out.closeTag("section")
        out.openTag("section")
        out.writeTag("title", _('Agenda:'))
        out.writeTag("line", params["meetingDescription"])
        out.closeTag("section")
        if booking.getHasAccessPassword():
            out.openTag("section")
            out.writeTag("title", _('Protection:'))
            out.writeTag("line", _('This WebEx meeting is protected by a password'))
            out.closeTag("section")
            if booking.showAccessPassword():
                out.openTag("section")
                out.writeTag("title", _('Meeting access password :'))
                out.writeTag("line", booking.getAccessPassword())
                out.closeTag("section")
        out.openTag("section")
        out.writeTag("title", _('Join URL:'))
        out.openTag("linkLineNewWindow")
        out.writeTag("href", booking.getUrl())
        out.writeTag("caption", "Click here to go to the WebEx meeting page")
        out.closeTag("linkLineNewWindow")
        out.closeTag("section")
        out.openTag("section")
        out.writeTag("title", _('Call-in toll free number (US/Canada):'))
        out.writeTag("line", booking.getPhoneNum())
        out.closeTag("section")
        out.openTag("section")
        out.writeTag("title", _('Call-in toll number: (US/Canada)'))
        out.writeTag("line", booking.getPhoneNumToll())
        out.closeTag("section")
        out.openTag("section")
        out.writeTag("title", _('Access code:'))
        out.writeTag("line", re.sub(r'(\d{3})(?=\d)',r'\1 ', str(booking._webExKey)[::-1])[::-1])
        out.closeTag("section")
        out.closeTag("information")

