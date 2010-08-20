# -*- coding: utf-8 -*-
##
## $Id: category.py,v 1.128 2009/06/26 12:13:17 cangelov Exp $
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

from copy import copy
from xml.sax.saxutils import quoteattr
from datetime import timedelta, datetime
import time
import os
import calendar
import MaKaC.webinterface.pages.conf_calendar as calend
import MaKaC.webinterface.pages.main as main
import MaKaC.webinterface.urlHandlers as urlHandlers
import MaKaC.webinterface.wcomponents as wcomponents
from MaKaC.webinterface.wcalendar import Overview
import MaKaC.conference as conference
from MaKaC.conference import CategoryManager
from MaKaC.common.Configuration import Config
import MaKaC.webinterface.wcalendar as wcalendar
import MaKaC.webinterface.linking as linking
from MaKaC import schedule
import MaKaC.common.info as info
from MaKaC.common.cache import CategoryCache
from MaKaC.i18n import _
from MaKaC.webinterface.common.timezones import TimezoneRegistry
from MaKaC.common.timezoneUtils import DisplayTZ,nowutc
from pytz import timezone


class WPCategoryBase ( main.WPMainBase ):
    
    def __init__( self, rh, categ ):
        main.WPMainBase.__init__( self, rh )
        self._target = categ 
        title = "Indico"
        if self._target:
            title = "Indico [%s]"%(self._target.getName() )
        self._setTitle(title)
        self._conf = None
    
#    def _createMenu( self ):
#        main.WPMainBase._createMenu( self )
#        c = self._target
#        
#        # enable event creation
#        if c and c.canCreateConference(self._getAW().getUser()):
#            if not c.hasSubcategories():
#                self._lectureOpt.setEnabled(True)
#                self._meetingOpt.setEnabled(True)
#                self._conferenceOpt.setEnabled(True)
#           
#                urlConference = urlHandlers.UHConferenceCreation.getURL(c)
#                urlConference.addParam("event_type","default")
#    
#                urlLecture = urlHandlers.UHConferenceCreation.getURL(c)
#                urlLecture.addParam("event_type","simple_event")
#    
#                urlMeeting = urlHandlers.UHConferenceCreation.getURL(c)
#                urlMeeting.addParam("event_type","meeting")
#    
#           
#                self._conferenceOpt.setURL( urlConference )
#                self._lectureOpt.setURL( urlLecture )
#                self._meetingOpt.setURL( urlMeeting )
#            else:
#                self._lectureOpt.setErrorMessage("msgNotFinalCategory")
#                self._meetingOpt.setErrorMessage("msgNotFinalCategory")
#                self._conferenceOpt.setErrorMessage("msgNotFinalCategory")


    def _currentCategory(self):
        return self._target

class WPCategoryDisplayBase( WPCategoryBase ):
    pass

## TODO: TO REMOVE ????
#    def _getFooter( self ):
#        """
#        """
#        wc = wcomponents.WFooter(isFrontPage=self._isFrontPage())
#        p = {}
#        if Config.getInstance().getShortCategURL():
#            if self._target.getId() != "0":
#                p["shortURL"] =  Config.getInstance().getShortCategURL() + self._target.getId()
#            else:
#                p["shortURL"] =  Config.getInstance().getBaseURL()
#        p["subArea"] = self._getSiteArea()
#        return wc.getHTML(p)

class WCategoryDisplay(wcomponents.WTemplated):
        
    def __init__( self, target, wfReg ):
        self._target = target
        self._wfReg = wfReg
        
    def _getMaterialHTML( self ):
        l = []
        for mat in self._target.getAllMaterialList():
            temp = wcomponents.WMaterialDisplayItem()
            url = urlHandlers.UHMaterialDisplay.getURL( mat )
            l.append( temp.getHTML( self._aw, mat, url ) )
        res = ""
        if l:
            res =   _("""
                        <span class="displayField"> _("Material"): %s</span>
                    """)%"".join( l )
        return res

    def getHTML( self, aw, params ):
        self._aw = aw
        return wcomponents.WTemplated.getHTML( self, params )
    
    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars["name"] = self._target.getName()
        vars["description"] = self._target.getDescription()
        vars["img"] = self._target.getIconURL()
        vars["categ"] = self._target;
        subcats = self._target.getSubCategoryList()
        confs = self._target.getConferenceList(True)
        if len(subcats) > 0:
            cl=wcomponents.WCategoryList( self._target )
            params = {"categoryDisplayURLGen": vars["categDisplayURLGen"], "material": self._getMaterialHTML()}
            vars["contents"] = cl.getHTML( self._aw, params )
        elif len(confs) > 0:
            cl = wcomponents.WConferenceList( self._target, self._wfReg )
            params = {"conferenceDisplayURLGen": vars["confDisplayURLGen"], "material": self._getMaterialHTML()}
            vars["contents"] = cl.getHTML( self._aw, params )
        else:
            vars["contents"] = _("This category is empty. Please start creating conferences or categories by using the top menu.") 
        mgrs=[]
        from MaKaC.user import Avatar
        for mgr in self._target.getManagerList():
            if isinstance(mgr, Avatar):
                mgrs.append(mgr.getAbrName())
        vars["managers"]=""
        if mgrs != []:
            vars["managers"]= "; ".join(mgrs)
        
        # TODO: Should be added to submenu
        if self._target.tasksAllowed() :
            vars["taskList"] = _("""<a href="%s"> _("Task List")</a>""")%urlHandlers.UHTaskList.getURL(self._target)
        else :
            vars["taskList"] = ""        
        
        return vars


class WPCategoryDisplay(WPCategoryDisplayBase):
    
    def __init__( self, rh, target, wfReg ):
        WPCategoryDisplayBase.__init__( self, rh, target )
        self._wfReg = wfReg
        if len(self._target.getSubCategoryList())==0:
            tzUtil = DisplayTZ(self._getAW(),target)#None,useServerTZ=1) 
            self._locTZ = tzUtil.getDisplayTZ()      

    def _getHeadContent( self ):
        # add RSS feed
        url = urlHandlers.UHCategoryToRSS.getURL(self._target)
        
        return WPCategoryDisplayBase._getHeadContent( self ) + \
        _("""<link rel="alternate" type="application/rss+xml" title= _("Indico RSS Feed") href="%s">""") % url
        
    def _getBody( self, params ):
        minfo = info.HelperMaKaCInfo.getMaKaCInfoInstance()
        tz = DisplayTZ(self._getAW(),self._target).getDisplayTZ()
        if minfo.isCacheActive() and tz == self._target.getTimezone():
            cache = CategoryCache({"categId":self._target.getId()})
            page = cache.getCachePage()
            if page != "":
                return page
        wc = WCategoryDisplay( self._target, self._wfReg )
        pars = { "categDisplayURLGen": urlHandlers.UHCategoryDisplay.getURL, \
                "confDisplayURLGen": urlHandlers.UHConferenceDisplay.getURL, \
                "allowUserModif": self._target.canModify( self._getAW() ), \
                "allowCreateEvent": self._target.canCreateConference(self._getAW().getUser()) }
        page = wc.getHTML( self._getAW(), pars )
        if minfo.isCacheActive() and tz == self._target.getTimezone():
            cache.saveCachePage(page)
        return page
        
    def _getNavigationDrawer(self):
        pars = {"target": self._target, "isModif": False}
        return wcomponents.WNavigationDrawer( pars )

class WOverviewBreak( wcomponents.WTemplated ):
    
    def __init__( self, aw, entry ):
        self._break = entry
        self._aw = aw

    def getVars( self ):
        tz = DisplayTZ(self._aw).getDisplayTZ()
        vars = wcomponents.WTemplated.getVars( self )
        vars["startTime"] = self._break.getAdjustedStartDate(tz).strftime("%H:%M")
        vars["title"] = self._break.getTitle()
        return vars


class WOverviewContribBase( wcomponents.WTemplated ):
    
    def __init__( self, aw, contrib, date, details="conference" ):
        self._aw = aw
        self._contrib = contrib
        self._date = date
        self._details = details
    
    def _getSpeakerText( self ):
        l = []
        if self._contrib.getSpeakerText()!="":
            l.append( self._contrib.getSpeakerText() )
        for av in self._contrib.getSpeakerList():
            l.append( "%s"%av.getAbrName() )
        speakers = ""
        if len(l)>0:
            speakers  = "(%s)"%"; ".join(l)
        return speakers

    def _getLocation( self ):
        loc = ""
        if self._contrib.getOwnLocation() != None:
            loc = self._contrib.getLocation().getName()
        if loc != "":
            loc = "(%s)"%loc
        room = ""
        if self._contrib.getOwnRoom() != None:
            room = self._contrib.getRoom().getName()
        if room != "":
            room = "(%s)"%room
        return "%s %s"%(loc, room)

    def getHTML( self, params={} ):
        return wcomponents.WTemplated.getHTML( self, params )

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        tz = DisplayTZ(self._aw).getDisplayTZ()
        vars["timezone"] = tz
        vars["startTime"] = self._contrib.getAdjustedStartDate(tz).strftime( "%H:%M" )
        vars["title"] = self._contrib.getTitle()
        vars["speakers"] = self._getSpeakerText()
        vars["location"] = self._getLocation()
        return vars


class WOverviewContribFullDisplay( WOverviewContribBase ):
    pass


class WOverviewContribMinDisplay( WOverviewContribBase ):
    pass


class WOverviewContribution:
    
    def __init__( self, aw, contrib, date, details="conference" ):
        self._comp = None
        
        """ This is needed for the future? The two
            templates are currently identical """
        
        if contrib.canAccess( aw ):
            self._comp = WOverviewContribFullDisplay( aw, \
                                                    contrib, \
                                                    date, \
                                                    details )
        else:
            self._comp = WOverviewContribMinDisplay( aw, \
                                                    contrib, \
                                                    date, \
                                                    details )
    def getHTML( self, params={} ):
        if not self._comp:
            return ""
        return self._comp.getHTML( params )


class WOverviewSessionBase( wcomponents.WTemplated ):
    
    def __init__( self, aw, session, date, details="conference" ):
        self._aw = aw
        self._session = session
        self._date = date
        self._details = details
    
    def _getConvenerText( self ):
        l = []
        if self._session.getConvenerText()!="":
            l.append( self._session.getConvenerText() )
        for av in self._session.getConvenerList():
            l.append( "%s"%av.getAbrName() )
        conveners = ""
        if len(l)>0:
            conveners = "(%s)"%"; ".join(l)
        return conveners

    def _getLocation( self ):
        loc = ""
        if self._session.getOwnLocation() != None:
            loc = self._session.getLocation().getName()
        room = ""
        if self._session.getOwnRoom() != None:
            url = linking.RoomLinker().getURL( self._session.getRoom(), \
                                                   self._session.getLocation() )
            room = self._session.getRoom().getName()
            if url != "":
                room = """<a href="%s"><font size="-2" color="blue">%s</font></a>"""%(url, room)
        if loc != "" or room != "":
            return "(%s %s)"%(loc, room)
        else:
            return ""

    def _getBreakItem( self, entry ):
        wc = WOverviewBreak( self._aw, entry )
        return wc.getHTML( {} )
    
    def _getDetails( self ):
        if self._details != "contribution":
            return ""
        res = []
        tz = DisplayTZ(self._aw).getDisplayTZ()
        for entry in self._session.getSchedule().getEntriesOnDay( self._date ):
            if self._details == "contribution":
                if isinstance( entry, schedule.LinkedTimeSchEntry) and \
                        isinstance( entry.getOwner(), conference.Contribution):
                    wc = WOverviewContribution( self._aw, \
                                                entry.getOwner(), \
                                                self._date, \
                                                self._details )
                    res.append( wc.getHTML( ) )
                elif isinstance( entry, schedule.BreakTimeSchEntry):
                    res.append( self._getBreakItem( entry ) )
        return "".join( res )

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        tz = DisplayTZ(self._aw).getDisplayTZ()
        vars["startTime"] = self._session.getStartDate().astimezone(timezone(tz)).strftime("%H:%M")
        conf=self._session.getConference()
        import MaKaC.webinterface.webFactoryRegistry as webFactoryRegistry
        wr = webFactoryRegistry.WebFactoryRegistry()
        wf = wr.getFactory(conf)
        if wf != None:
            type = wf.getId()
        else:
            type = "conference"
        if type != 'meeting':
            vars["title"] = self._session.getTitle()
            vars["titleUrl"] = None
        else:
            vars["title"] = self._session.getTitle()
            vars["titleUrl"] = """%s#%s""" % (urlHandlers.UHConferenceDisplay.getURL(conf), self._session.getId())
        vars["conveners"] = self._getConvenerText()
        vars["location"] = self._getLocation()
        vars["details"] = self._getDetails()
        return vars

class WOverviewSessionSlot( WOverviewSessionBase ):
    
    def __init__( self, aw, slot, date, details="conference" ):
        self._aw = aw
        self._session = slot.getSession()
        self._slot = slot
        self._date = date
        self._details = details
    
    def _getDetails( self ):
        if self._details != "contribution":
            return ""
        res = []
        tz = DisplayTZ(self._aw).getDisplayTZ()
        for entry in self._slot.getSchedule().getEntriesOnDay( self._date ):
            if self._details == "contribution":
                if isinstance( entry, schedule.LinkedTimeSchEntry) and type(entry.getOwner()) is conference.Contribution:
                    wc = WOverviewContribution( self._aw, \
                                                entry.getOwner(), \
                                                self._date, \
                                                self._details )
                    res.append( wc.getHTML( ) )
                elif isinstance( entry, schedule.BreakTimeSchEntry):
                    res.append( self._getBreakItem( entry ) )
        return "".join( res )

class WOverviewSessionFullDisplay( WOverviewSessionBase ):
    pass


class WOverviewSessionMinDisplay( WOverviewSessionBase ):
    
    def _getBreakItem( self, entry ):
        return ""


class WOverviewSession:
    
    def __init__( self, aw, session, date, details="conference" ):
        self._comp = None
        if session.canAccess( aw ):
            self._comp = WOverviewSessionFullDisplay( aw, \
                                                    session, \
                                                    date, \
                                                    details )
        else:
            self._comp = WOverviewSessionMinDisplay( aw, \
                                                    session, \
                                                    date, \
                                                    details )
    def getHTML( self, params ):
        if not self._comp:
            return ""
        return self._comp.getHTML( params )
        

class WOverviewConfBase( wcomponents.WTemplated ):
    
    def __init__( self, aw, conference, date, url, icons, details="conference" ):
        self._conf = conference
        self._url = url
        self._aw = aw
        self._details = details
        self._date = date
        self._icons = icons
        
    
    def _getChairText( self ):
        l = []
        if self._conf.getChairmanText()!="":
            l.append( self._conf.getChairmanText() )
        for av in self._conf.getChairList():
            l.append( "%s"%av.getFullName() )
        chairs = ""
        if len(l)>0:
            chairs = "(%s)"%"; ".join(l)
        return chairs

    def _getLocation( self ):
        loc = ""
        if self._conf.getLocation() != None:
            loc = self._conf.getLocation().getName()
        room = ""
        if self._conf.getRoom() != None:
            url = linking.RoomLinker().getURL( self._conf.getRoom(), \
                                                    self._conf.getLocation() )
            room = self._conf.getRoom().getName()
            if url != "":
                room = """<a href="%s" style="font-size: 0.9em">%s</a>"""%(url, room)
        if loc != "" or room != "":
            return "(%s %s)"%(loc, room)
        else:
            return ""

    def _getBreakItem( self, entry ):
        wc = WOverviewBreak( self._aw, entry )
        return wc.getHTML( {} )

    def _getDetails( self ):
        if self._details == "conference":
            return ""
        res = []
        tz = DisplayTZ(self._aw,useServerTZ=1).getDisplayTZ()
        for entry in self._conf.getSchedule().getEntriesOnDay( self._date ):
            if isinstance( entry, schedule.LinkedTimeSchEntry) and \
                        isinstance( entry.getOwner(), conference.Session ) and entry.getOwner().canView(self._aw):
                wc = WOverviewSession( self._aw, \
                                        entry.getOwner(), \
                                        self._date, \
                                        self._details )
                res.append( wc.getHTML({}) )
            elif isinstance( entry, schedule.LinkedTimeSchEntry) and \
                        isinstance( entry.getOwner(), conference.SessionSlot ) and entry.getOwner().canView(self._aw):
                wc = WOverviewSessionSlot( self._aw, \
                                        entry.getOwner(), \
                                        self._date, \
                                        self._details )
                res.append( wc.getHTML({}) )
            elif self._details == "contribution":
                if isinstance(entry, conference.ContribSchEntry) or  \
                    isinstance( entry, schedule.LinkedTimeSchEntry) and isinstance(entry.getOwner(), conference.Contribution) and entry.getOwner().canView(self._aw):
                    wc = WOverviewContribution( self._aw, \
                                                entry.getOwner(), \
                                                self._date, \
                                                self._details )
                    res.append( wc.getHTML( ) )
                elif isinstance( entry, schedule.BreakTimeSchEntry):
                    res.append( self._getBreakItem( entry ) )
        return "".join( res )
    
    def _getIcon( self ):
        confid = self._conf.getId()
        iconHtml = ""
        for icon in self._icons.keys():
            if confid in self._icons[icon]:
                cm=CategoryManager()
                categ = cm.getById(str(icon))
                iconHtml += """<img src="%s" width="16" height="16" alt="categ" onmouseover="IndicoUI.Widgets.Generic.tooltip(this, event, '%s')" />""" %(urlHandlers.UHCategoryIcon.getURL(categ), categ.getName())
        return iconHtml

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        tz = DisplayTZ(self._aw,useServerTZ=1).getDisplayTZ()
        vars["startTime"] = self._conf.calculateDayStartTime(self._date).strftime("%H:%M")
        vars["timezone"] = tz
        vars["title"] = self._conf.getTitle()
        if self._conf.isProtected():
            vars["title"] += """&nbsp;<img src=%s style="vertical-align: middle; border: 0;">""" % Config.getInstance().getSystemIconURL("protected")
        vars["url"] = self._url
        vars["chairs"] = self._getChairText()
        vars["location"] = self._getLocation()
        vars["details"] = self._getDetails()
        vars["icon"] = self._getIcon()
        return vars


class WOverviewConfFullDisplay( WOverviewConfBase ):
    pass

class WOverviewConfMinDisplay( WOverviewConfBase ):
    
    def _getDetails( self ):
        return ""

    def _getBreakItem( self, entry ):
        return ""


class WOverviewConferenceItem:
    
    def __init__(self, aw, conference, date, displayURL, icons, details="conference"):
        self._comp = None
        if details=="conference" or conference.canAccess( aw ):
            self._comp = WOverviewConfFullDisplay( aw, \
                                                    conference, \
                                                    date, \
                                                    displayURL, \
                                                    icons, \
                                                    details )
        else:
            self._comp = WOverviewConfMinDisplay( aw, \
                                                    conference, \
                                                    date, \
                                                    displayURL, \
                                                    icons, \
                                                    details )

    def getHTML( self, params ):
        if not self._comp:
            return ""
        return self._comp.getHTML( params )


class WDayOverview(wcomponents.WTemplated):
    
    def __init__( self, ow ):
        self._ow = ow

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        prevOW = self._ow.getOverviewPrevPeriod()
        prevsel = urlHandlers.UHCategoryOverview.getURLFromOverview( prevOW )
        nextOW = self._ow.getOverviewNextPeriod()
        nextsel = urlHandlers.UHCategoryOverview.getURLFromOverview( nextOW )
        pprevOW = self._ow.getOverviewPrevBigPeriod()
        pprevsel = urlHandlers.UHCategoryOverview.getURLFromOverview( pprevOW )
        nnextOW = self._ow.getOverviewNextBigPeriod()
        nnextsel = urlHandlers.UHCategoryOverview.getURLFromOverview( nnextOW )
        vars["date"] = """<a href="%s">&lt;&lt;</a>&nbsp;&nbsp;<a href="%s">&lt;</a>&nbsp;&nbsp;%s&nbsp;&nbsp;<a href="%s">&gt;</a>&nbsp;&nbsp;<a href="%s">&gt;&gt;</a>""" % (\
                pprevsel, \
                prevsel,\
                self._ow.getDate().strftime("%A %d %B %Y"), \
                nextsel,\
                nnextsel)
        l = []
        confs = self._ow.getConferences()
        confs.sort(lambda x,y: cmp(x.calculateDayStartTime(self._ow.getDate()).time(),y.calculateDayStartTime(self._ow.getDate()).time()))
        for conf in confs:
            oi = WOverviewConferenceItem( self._ow.getAW(), \
                                            conf, \
                                            self._ow.getDate(), \
                                            vars["displayConfURLGen"]( conf ),\
                                            self._ow._cal.getIcons(), \
                                            self._ow.getDetailLevel() )
            l.append( oi.getHTML( {} ) )
        if len(confs)==0:
            l.append( _("There are no conferences on the selected day"))
        vars["items"] = "".join(l)
        return vars

class WWeekOverview(wcomponents.WTemplated):
    
    def __init__( self, ow ):
        self._ow = ow

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        prevOW = self._ow.getOverviewPrevPeriod()
        prevsel = urlHandlers.UHCategoryOverview.getURLFromOverview( prevOW )
        nextOW = self._ow.getOverviewNextPeriod()
        nextsel = urlHandlers.UHCategoryOverview.getURLFromOverview( nextOW )
        
        startDate = """<a href="%s">&lt;</a>&nbsp;&nbsp;%s""" % (\
                prevsel,\
                self._ow.getStartDate().strftime("%A %d %B %Y"))
        endDate = """%s&nbsp;&nbsp;<a href="%s">&gt;</a>""" %(\
                self._ow.getEndDate().strftime("%A %d %B %Y"),\
                nextsel)
        vars["dates"] = """%s &nbsp;&ndash;&nbsp; %s"""%(startDate, endDate)
        
        inc = timedelta( 1 )
        sd = self._ow.getStartDate()
        idx = 0
        while sd <= self._ow.getEndDate():
            vars["date%i"%idx] = sd.strftime( "%a %d/%m" )
            res = []
            confs = self._ow.getConferences( sd )
            confs.sort(lambda x,y: cmp(x.calculateDayStartTime(sd).time(),y.calculateDayStartTime(sd).time()))
            for conf in confs:
                wc = WOverviewConferenceItem( self._ow.getAW(), \
                                            conf, \
                                            sd, \
                                            vars["displayConfURLGen"]( conf ),\
                                            self._ow._cal.getIcons(), \
                                            self._ow.getDetailLevel() )
                res.append( wc.getHTML( {} ) )
           
            if res==[]:
                res.append("<tr><td></td></tr>")
            vars["item%i"%idx] = "".join( res )
            sd += inc
            idx += 1
        vars["items"] = ""
        return vars

# This class is currently not used since the list of conference that we
# iterate over is always zero for some reason. Remove the class in the future
# or fix it?
class WNextWeekOverview(wcomponents.WTemplated):
    
    def __init__( self, ow ):
        self._ow = ow

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )

        startDate = """%s""" % self._ow.getStartDate().strftime("%A %d %B %Y")
        endDate = """%s""" % self._ow.getEndDate().strftime("%A %d %B %Y")
        vars["dates"] = """%s &nbsp;&ndash;&nbsp; %s"""%(startDate, endDate)

        inc = timedelta( 1 )
        sd = self._ow.getStartDate()
        idx = 0
        while sd <= self._ow.getEndDate():
            vars["date%i"%idx] = sd.strftime( "%a %d/%m" )
            res = []
            confs = self._ow.getConferences( sd )
            confs.sort(lambda x,y: cmp(x.calculateDayStartTime(sd).time(),y.calculateDayStartTime(sd).time()))
            for conf in confs:
                wc = WOverviewConferenceItem( self._ow.getAW(), \
                                            conf, \
                                            sd, \
                                            vars["displayConfURLGen"]( conf ),\
                                            self._ow._cal.getIcons(), \
                                            self._ow.getDetailLevel() )
                res.append( wc.getHTML( {} ) )
                raise wc
            if res==[]:
                res.append("<tr><td></td></tr>")
            vars["item%i"%idx] = "".join( res )
            sd += inc
            idx += 1
        vars["items"] = ""
        return vars


class WMonthOverview(wcomponents.WTemplated):

    def __init__( self, ow ):
        self._ow = ow

    def _getDayCell( self, day=None ):
        if day == None:
            return """<td>&nbsp;</td>"""
        else:
            res = []
            confs = day.getConferences()
            confs.sort(lambda x,y: cmp(x.calculateDayStartTime(day.getDate()).time(),y.calculateDayStartTime(day.getDate()).time()))
            for conf in confs:
                wc = WOverviewConferenceItem( self._ow.getAW(), \
                                            conf, \
                                            day.getDate(), \
                                            self._displayConfURLGen( conf ),\
                                            self._ow._cal.getIcons(), \
                                            self._ow.getDetailLevel() )
                res.append( wc.getHTML( {} ) )
            return """
                <td valign="top" bgcolor="#ECECEC">
                    <table width="100%%">
                        <tr>
                            <td align="center">
                                <strong style="font-size: 1.3em; color: #888;">%s</strong>
                            </td>
                        </tr>
                        <tr>
                            <td valign="top">%s</td>
                        </tr>
                    </table>
                </td>"""%(day.getDayNumber(), "".join(res))

    def _getMonth( self ):
        dl = self._ow.getDayList()
        month = ""
        week = ""
        for i in range( dl[0].getWeekDay() ):
            week = "%s%s"%(week, self._getDayCell())
        for day in self._ow.getDayList():
            week = "%s%s"%(week, self._getDayCell( day ))
            if day.getWeekDay() == 6:
                month = """%s<tr>%s</tr>"""%(month, week)
                week = ""
        
        for i in range( 6-dl[-1].getWeekDay() ):
            week = "%s%s"%(week, self._getDayCell())
        return """%s<tr>%s</tr>"""%(month, week)
            

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        prevOW = self._ow.getOverviewPrevPeriod()
        prevsel = urlHandlers.UHCategoryOverview.getURLFromOverview( prevOW )
        nextOW = self._ow.getOverviewNextPeriod()
        nextsel = urlHandlers.UHCategoryOverview.getURLFromOverview( nextOW )
        pprevOW = self._ow.getOverviewPrevBigPeriod()
        pprevsel = urlHandlers.UHCategoryOverview.getURLFromOverview( pprevOW )
        nnextOW = self._ow.getOverviewNextBigPeriod()
        nnextsel = urlHandlers.UHCategoryOverview.getURLFromOverview( nnextOW )
        startDate = """<a href="%s">&lt;&lt;</a>&nbsp;&nbsp;<a href="%s">&lt;</a>&nbsp;&nbsp;&nbsp;%s""" % (\
                pprevsel,\
                prevsel,\
                self._ow.getStartDate().strftime("%A %d %B %Y"))
        endDate = """%s&nbsp;&nbsp;&nbsp;<a href="%s">&gt;</a>&nbsp;&nbsp;<a href="%s">&gt;&gt;</a>""" %(\
                self._ow.getEndDate().strftime("%A %d %B %Y"),\
                nextsel,\
                nnextsel)
        vars["dates"] = """%s &nbsp;&ndash;&nbsp; %s"""%(startDate, endDate)

        dayNames = [ _("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), \
                        _("Saturday"), _("Sunday") ]
        #if calendar.SUNDAY == calendar.firstweekday():
        #    dayNames.remove( "Sunday" )
        #    dayNames.insert( "0", "Sunday" )
        for name in dayNames:
            vars["nameDay%i"%dayNames.index(name)] = name
        self._displayConfURLGen = vars["displayConfURLGen"]
        vars["items"] = self._getMonth()
        return vars


class WCategoryOverview(wcomponents.WTemplated):
    
    def __init__( self, ow, aw ):
        self._categ = ow.getCategoryList()[0]
        self._ow = ow
        self._aw = aw

    def _getDetailLevelOpts( self ):
        l = []
        for dl in self._ow.getAllowedDetailLevels():
            selected = ""
            if dl == self._ow.getDetailLevel():
                selected = "selected"
            if dl == "conference":
                dltext = "agenda"
            else:
                dltext = dl
            l.append("""<option value="%s" %s>%s</option>"""%( dl, selected, dltext ))
        return "".join(l)

    def _getKey( self, vars):
        l = []
        icons = self._ow._cal.getIcons().keys()
        if len(icons) > 0:
            for icon in icons:
                cm= CategoryManager()
                categ=cm.getById(str(icon))
                otherOW = self._ow.getOverviewOtherCateg(categ)
                a=(""" <a href="%s" style="font-size: 1.0em;"><img src="%s" width="16" height="16" border="0" alt="category">&nbsp;%s</a>  <BR>""" %(\
                                        vars["categOverviewURLGen"]( otherOW ),\
                                        urlHandlers.UHCategoryIcon.getURL(categ),\
                                        categ.getName().replace(" ","&nbsp;")))
                if not a in l:
                    l.append(a)
        return "". join(l)
            
    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        l = self._ow.getLocator()
        del l["detail"]
        del l["period"]
        del l["day"]
        del l["month"]
        del l["year"]
        
        vars["selDay"] = ""
        vars["selWeek"] = ""
        vars["selNextWeek"] = ""
        vars["selMonth"] = ""
        vars["selYear"] = ""

        vars["detailLevelOpts"] = self._getDetailLevelOpts()
        
        if isinstance( self._ow, wcalendar.MonthOverview ):
            displayOW = WMonthOverview( self._ow )
            vars["selMonth"] = "selected"
        elif isinstance( self._ow, wcalendar.WeekOverview ):
            displayOW = WWeekOverview( self._ow )
            vars["selWeek"] = "selected"
            
        #  This will not happen since the option in the selection
        #  box in the user interface has been removed. Can be readded
        #  in the future if needed.
        elif isinstance( self._ow, wcalendar.NextWeekOverview ):
            displayOW = WNextWeekOverview( self._ow )
            vars["selNextWeek"] = "selected"
        else:
            displayOW = WDayOverview( self._ow )
            vars["selDay"] = "selected"

        p = { "displayConfURLGen": vars["displayConfURLGen"] }
        vars["overview"] = displayOW.getHTML( p )

        vars["locator"] = l.getWebForm()
        vars["key"] = self._getKey(vars)
        
        vars["day"] = self._ow.getDate().day
        vars["month"] = self._ow.getDate().month
        vars["year"] = self._ow.getDate().year

        return vars
    
    def _getWeekDays(self):
        """returns a list with the current week days"""
        
        year=int(self._ow.getDate().year)
        month=int(self._ow.getDate().month)
        day=int(self._ow.getDate().day)
        daynumber=int(calendar.weekday(year,month,day))
        
        date = self._ow.getDate() - timedelta(daynumber)
        delta = timedelta(1)
        res = []
        for i in range(7):
            res.append((str(date.day)+"-"+str(date.month)+"-"+str(date.year)))
            date += delta
        
        #if daynumber == 0:
        #    res = [(str(day)+"-"+str(month)+"-"+str(year))]
        #    i=1
        #    while i <= 6:
        #        if (day+i)<32 and (month==8 or month==1 or month==3 or month==5 or month==7 or month==10):
        #            res+=[(str(day+i)+"-"+str(month)+"-"+str(year))]
        #        if (day+i)<31 and (month==4 or month==6 or month==9 or month==11):
        #            res+=[(str(day+i)+"-"+str(month)+"-"+str(year))]
        #        if (day+i)<29 and month==2 and (year %4!=0 or (year %4 ==0 and year %100==0)):
        #            res+=[(str(day+i)+"-"+str(month)+"-"+str(year))]
        #        if (day+i)<30 and month==2 and ((year%4==0 and year%100!=0) or year%400==0):
        #            res+=[(str(day+i)+"-"+str(month)+"-"+str(year))]
        #            
        #        i+=1
        #else:
        #    res = [(str(day)+"-"+str(month)+"-"+str(year))]
        #    i=1
        #    while i <= 7:
        #        j = day+7-daynumber-i          #day+i-(daynumber+1)
        #        if j>0 and j <32 and (month==8 or month==1 or month==3 or month==5 or month==7 or month==10):
        #            
        #            res+=[(str(j)+"-"+str(month)+"-"+str(year))]
        #        
        #        if j>0 and j<31 and (month==4 or month==6 or month==9 or month==11):
        #            res+=[(str(j)+"-"+str(month)+"-"+str(year))]
        #        
        #        if j>0 and j<29 and month==2 and ((year %4!=0) or (year %4 ==0 and year %100==0)):
        #            res+=[(str(j)+"-"+str(month)+"-"+str(year))]
        #        
        #        if j>0 and j<30 and month==2 and ((year%4==0 and year%100!=0) or year%400==0):
        #            res+=[(str(j)+"-"+str(month)+"-"+str(year))]
        #            
        #        i+=1
                                 
        return res
    
    


    def _getNextWeekDays(self):
        
     
        y=int(self._ow.getDate().year)
        m=int(self._ow.getDate().month)
        d=int(self._ow.getDate().day)
        
        res=[]
        i=0
        while i<=6:
            
            if (d+i)<=31 and (m==8 or m==1 or m==3 or m==5 or m==7 or m==10):
                res+=[str(d+i)+"-"+str(m)+"-"+str(y)]
            if (d+i)<=30 and (m==4 or m==6 or m==9 or m==11):
                res+=[str(d+i)+'-'+str(m)+'-'+str(y)]
            if (d+i)<=28 and m==2 and ((y%4!=0) or (y %4 ==0 and y %100==0)):
                res+=[(str(d+i)+"-"+str(m)+"-"+str(y))]
            if (d+i)<30 and m==2 and ((y%4==0 and y%100!=0) or y%400==0):
                res+=[(str(d+i)+"-"+str(m)+"-"+str(y))]
            i+=1
        
        j=0    
        if d<7 and len(res)<7:
            while j<(7-len(res)):
                res+=[(str(d+i+j)+"-"+str(m)+"-"+str(y))]
                j+=1
                
                
        return res
    
    def _whichPeriod(self,vars):
        
        
        if vars["selDay"]=="selected":
            return "day"
        if vars["selWeek"]=="selected":
            return "week"
        if vars["selNextWeek"]=="selected":
            return "nextweek"
        if vars["selMonth"]=="selected":
            return "month"

    def _getMonthDays(self):
        year=int(self._ow.getDate().year)
        month=int(self._ow.getDate().month)
        res=[]
        for day in range(1,calendar.monthrange(year,month)[1]+1):
            res+=[str(day)+'-'+str(month)+'-'+str(year)]
    
        return res

class WPCategOverview( WPCategoryDisplayBase ):
    
    def __init__( self, rh, categ, ow ):
        WPCategoryDisplayBase.__init__( self, rh, categ )
        self._ow = ow
        self._categ = categ
        self._locTZ = DisplayTZ(self._getAW(),None,useServerTZ=1).getDisplayTZ()  
        
    def _getTitle(self):
        return WPCategoryDisplayBase._getTitle(self) + " - " + _("Events Display")    
    
    def _getHeadContent( self ):
        # add RSS feed
        if self._ow.getDate().date() == nowutc().astimezone(timezone(self._locTZ)).date():
            url = urlHandlers.UHCategOverviewToRSS.getURL(self._categ)
            return _("""<link rel="alternate" type="application/rss+xml" title= _("Indico RSS Feed") href="%s">""") % url
        return ""

    def _getBody( self, params ):
        if self._categ.getId() ==  "0" and type(self._ow) is Overview and self._ow.getDate().date() == nowutc().astimezone(timezone(self._locTZ)).date():
            path = os.path.join(Config.getInstance().getXMLCacheDir(),"categOverview")
            currenttime = int(time.mktime(time.strptime((datetime.now()-timedelta(minutes=60)).strftime("%a %b %d %H:%M:%S %Y"))))
            if os.path.exists(path) and os.path.getmtime(path) > currenttime:
                fp = file(path, 'rb')
                cache = fp.read()
                fp.close()
                return cache
            else:
                wc = WCategoryOverview( self._ow, self._rh.getAW())
                pars = { "postURL": urlHandlers.UHCategoryOverview.getURL(), \
                "displayConfURLGen": urlHandlers.UHConferenceDisplay.getURL, \
                "categOverviewURLGen": urlHandlers.UHCategoryOverview.getURLFromOverview }
                cache = wc.getHTML( pars )
                fp = file(path, 'wb')
                fp.write(cache)
                fp.close()
                return cache
        else:
            wc = WCategoryOverview( self._ow, self._rh.getAW())
            pars = { "postURL": urlHandlers.UHCategoryOverview.getURL(), \
                     "displayConfURLGen": urlHandlers.UHConferenceDisplay.getURL, \
                     "categDisplayURL": urlHandlers.UHCategoryDisplay.getURL(self._categ), \
                     "categOverviewURLGen": urlHandlers.UHCategoryOverview.getURLFromOverview, \
                     "categoryTitle": self._categ.getTitle() }
            return wc.getHTML( pars )
    
    def _getNavigationDrawer(self):
        link = [{"url": urlHandlers.UHCategoryOverview.getURL(self._target), "title": _("Events overview"), "type": "Overview"}]
        pars = {"target": self._target, "isModif": False}
        return wcomponents.WNavigationDrawer( pars, appendPath = link )
    
class WCategoryMap(wcomponents.WTemplated):
    
    def __init__( self, categ ):
        self._categ = categ
        
    def getCategMap( self, categ ):
        res = []
        if len(categ.getSubCategoryList()) > 0:
            res.append("<ul>")
            for subcat in categ.getSubCategoryList():
                res.append("<li><a href='%s'>%s</a>"% (urlHandlers.UHCategoryDisplay.getURL(subcat), subcat.getName()))
                if subcat.hasAnyProtection(): 
                    res.append("""&nbsp;<span style="font-size: 0.8em; color: gray;">(%s)</span>"""% _("protected"))
                res.append(self.getCategMap(subcat))
            res.append("</ul>")
        return "".join(res)
                
    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars['categName'] =  self._categ.getName()
        vars["categDisplayURL"] = urlHandlers.UHCategoryDisplay.getURL(self._categ)
        vars['map'] = self.getCategMap(self._categ)
        return vars
        
class WPCategoryMap( WPCategoryDisplayBase ):
    
    def __init__( self, rh, categ ):
        WPCategoryDisplayBase.__init__( self, rh, categ )
        
    def _getTitle(self):
        return WPCategoryDisplayBase._getTitle(self) + " - " + _("Category Map")    

    def _getBody( self, params ):
        wc = WCategoryMap( self._target )
        pars = {}
        return wc.getHTML( pars )
        
    def _getNavigationDrawer(self):
        link = [{"url": urlHandlers.UHCategoryMap.getURL(self._target), "title": _("Category map"), "type": "Map"}]
        pars = {"target": self._target, "isModif": False}
        return wcomponents.WNavigationDrawer( pars, appendPath = link )

class WCategoryStatistics(wcomponents.WTemplated):
        
    def __init__( self, target, wfReg, stats ):
        self.__target = target
        self._wfReg = wfReg
        self._stats = stats

    def getHTML( self, aw ):
        self._aw = aw
        return wcomponents.WTemplated.getHTML( self )
    
    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars["name"] = self.__target.getName()
        vars["img"] = self.__target.getIconURL()
        vars["categDisplayURL"] = urlHandlers.UHCategoryDisplay.getURL(self.__target)
        if self._stats != None:
            stats = []
            # Number of events:
            if self._stats["events"] != None:
                wcsl=wcomponents.WCategoryStatisticsList( _("Number of events"), self._stats["events"] )
                stats.append(wcsl.getHTML( self._aw ))
                # Number of contributions:
                if self._stats["contributions"] != {}:
                    wcsl=wcomponents.WCategoryStatisticsList( _("Number of contributions"), self._stats["contributions"] )
                    stats.append(wcsl.getHTML( self._aw ))
                else:
                    stats.append( _("""<b> _("Number of contributions"): 0</b>"""))
                stats.append( _("""<b> _("Number of resources"): %s</b>""")%self._stats["resources"])
                vars["updated"] = self._stats["updated"].strftime("%d %B %Y %H:%M")
            else:
                stats.append(_("""<b> _("No statistics for the events").</b>"""))
                stats.append(_("""<b> _("No statistics for the contributions").</b>"""))
                stats.append(_("""<b> _("No statistics for the resources").</b>"""))
                vars["updated"] = nowutc().strftime("%d %B %Y %H:%M")
            vars["contents"] = "<br><br>".join( stats )
        else:
            vars["contents"] = _("This category doesn't contain any event. No statistics are available.")
            vars["updated"] = nowutc().strftime("%d %B %Y %H:%M")
        return vars

class WPCategoryStatistics( WPCategoryDisplayBase ):
    
    def __init__( self, rh, target, wfReg, stats ):
        WPCategoryDisplayBase.__init__( self, rh, target )
        self._wfReg = wfReg
        self._stats = stats
        
    def _getTitle(self):
        return WPCategoryDisplayBase._getTitle(self) + " - " + _("Category Statistics")    
    
    def _getBody( self, params ):
        wcs = WCategoryStatistics( self._target, self._wfReg, self._stats )
        return wcs.getHTML( self._getAW() )
        
    def _getNavigationDrawer(self):
        link = [{"url": urlHandlers.UHCategoryStatistics.getURL(self._target), "title": _("Category statistics"), "type": "Statistics"}]
        pars = {"target": self._target, "isModif": False}
        return wcomponents.WNavigationDrawer( pars, appendPath = link )

class WEventTypeSelectionItem(wcomponents.WTemplated):
    
    def __init__(self, webFactory ):
        self.__webFactory = webFactory

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars["id"] = self.__webFactory.getId()
        vars["name"] = self.__webFactory.getName()
        vars["description"] = self.__webFactory.getDescription()
        return vars


class WEventTypeSelection(wcomponents.WTemplated):

    def __init__( self, targetCateg, webFactoryList ):
        self.__webFactoryList = webFactoryList
        self.__categ = targetCateg

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        l = []
        for webFact in self.__webFactoryList:
            l.append( WEventTypeSelectionItem( webFact ).getHTML() )
        vars["eventTypes"] = "".join(l)
        return vars


class WPConferenceCreationSelectType( WPCategoryDisplayBase ):
    
    def _getBody( self, params ):
        #p = { "categDisplayURLGen": urlHandlers.UHCategoryDisplay.getURL }
        wp = WEventTypeSelection( self._target,\
                                                params.get("wfs", [] ) )
        p = {"postURL":  urlHandlers.UHConferenceCreation.getURL(self._target)}
        return "%s"%wp.getHTML( p )


                       
#---------------------------------------------------------------------------
    
class WConferenceCreation( wcomponents.WTemplated ):
    
    def __init__( self, targetCateg, type="", rh = None ):
        self._categ = targetCateg
        self._type = type
        self._rh = rh

    
    def getVars(self):
        vars = wcomponents.WTemplated.getVars( self )        
        navigator = ""
        vars["title"] = vars.get("title","")
        vars["description"] = vars.get("description","")
        vars["keywords"] = vars.get("keywords","")
        vars["contactInfo"] = vars.get("contactInfo","")
        av=self._rh._getUser()
        tz=av.getTimezone()
        now = nowutc().astimezone(timezone(tz))
        vars["sDay"] = vars.get("sDay",now.day)
        vars["sMonth"] = vars.get("sMonth",now.month)
        vars["sYear"] = vars.get("sYear",now.year)
        vars["sHour"] = vars.get("sHour","8")
        vars["sMinute"] = vars.get("sMinute","00")
        vars["eDay"] = vars.get("eDay",now.day)
        vars["eMonth"] = vars.get("eMonth",now.month)
        vars["eYear"] = vars.get("eYear",now.year)
        vars["eHour"] = vars.get("eHour","18")
        vars["eMinute"] = vars.get("eMinute","00")
        
        vars["sDay_"] = {}
        vars["sMonth_"] = {}
        vars["sYear_"] = {}
        vars["sHour_"] = {}
        vars["sMinute_"] = {}
        vars["dur_"] = {}
            
        for i in range(0,10):
            vars["sDay_"][i] = vars.get("sDay_%s"%i,now.day)
            vars["sMonth_"][i] = vars.get("sMonth_%s"%i,now.month)
            vars["sYear_"][i] = vars.get("sYear_%s"%i,now.year)
            vars["sHour_"][i] = vars.get("sHour_%s"%i,"8")
            vars["sMinute_"][i] = vars.get("sMinute_%s"%i,"00")
            vars["dur_"][i] = vars.get("dur_%s"%i,"60")
        vars["nbDates"] = vars.get("nbDates",1)
        minfo = info.HelperMaKaCInfo.getMaKaCInfoInstance()
        seltitle = minfo.getTimezone()
        if self._categ:
            seltitle= self._categ.getTimezone()
        vars["timezoneOptions"] = TimezoneRegistry.getShortSelectItemsHTML(seltitle)
        vars["locationName"] = vars.get("locationName","")
        vars["locationAddress"] = vars.get("locationAddress","")
        vars["roomName"] = vars.get("locationRoom","")
        #vars["locator"] = self._categ.getLocator().getWebForm()
        vars["categ"] = {"id":"", "title":_("-- please, choose a category --") }
        if self._categ and not self._categ.hasSubcategories():
            vars["categ"] = {"id":self._categ.getId(), "title":self._categ.getTitle()}
        vars["nocategs"] = False
        if not CategoryManager().getRoot().hasSubcategories():
            vars["nocategs"] = True
            rootcateg = CategoryManager().getRoot()
            vars["categ"] = {"id":rootcateg.getId(), "title":rootcateg.getTitle()}
        #vars["event_type"] = ""
        vars["navigator"] = navigator
        vars["orgText"] = ""
        if vars.get("orgText","") != "":
            vars["orgText"] = vars.get("orgText","")
        elif self._rh._getUser():
            vars["orgText"] = self._rh._getUser().getStraightFullName()
        vars["chairText"] = vars.get("chairText","")
        vars["supportEmail"] = vars.get("supportEmail","")
        styleMgr = info.HelperMaKaCInfo.getMaKaCInfoInstance().getStyleManager()
        stylesheets = styleMgr.getStylesheetListForEventType(self._type)
        styleoptions = ""
        for stylesheet in stylesheets:
            defStyle = ""
            if self._categ:
                defStyle = self._categ.getDefaultStyle(self._type)
            if defStyle == "":
                defStyle = styleMgr.getDefaultStylesheetForEventType(self._type)
            if stylesheet == defStyle:
                selected = "selected"
            else:
                selected = ""
            styleoptions += "<option value=\"%s\" %s>%s</option>" % (stylesheet,selected,styleMgr.getStylesheetName(stylesheet))
        vars["styleOptions"] = styleoptions
        
        vars["chairpersonDefined"] = vars.get("chairpersonDefined", [])
        
        vars["useRoomBookingModule"] = minfo.getRoomBookingModuleActive()
        
        return vars
        
#---------------------------------------------------------------------------            
    
class WPConferenceCreationMainData( WPCategoryDisplayBase ):

    def getJSFiles(self):
        return WPCategoryDisplayBase.getJSFiles(self) + \
               self._includeJSPackage('Management')

    def _getHeader( self ):
        """
        """
        wc = wcomponents.WHeader( self._getAW() )
        return wc.getHTML( { "subArea": self._getSiteArea(), \
                             "loginURL": self._escapeChars(str(self.getLoginURL())),\
                             "logoutURL": self._escapeChars(str(self.getLogoutURL())),\
                             "loginAsURL": self.getLoginAsURL() } )

    def _getNavigationDrawer(self):
        pars = {"target": self._target, "isModif": False}
        return wcomponents.WNavigationDrawer( pars )
   
    def _getWComponent( self ):
        return WConferenceCreation( self._target, "", self._rh )

    def _getBody( self, params ):
        ## TODO: TO REMOVE?????????
        #p = { "categDisplayURLGen": urlHandlers.UHCategoryDisplay.getURL }       
        wc = self._getWComponent()
        params.update({"postURL": urlHandlers.UHConferencePerformCreation.getURL() })
        return "%s"%wc.getHTML( params )

class WPCategoryModifBase( WPCategoryBase ):

    def getJSFiles(self):
        return WPCategoryBase.getJSFiles(self) + \
               self._includeJSPackage('Management')

    def _getHeader( self ):
        """
        """
        wc = wcomponents.WHeader( self._getAW() )
        return wc.getHTML( { "subArea": self._getSiteArea(), \
                             "loginURL": self._escapeChars(str(self.getLoginURL())),\
                             "logoutURL": self._escapeChars(str(self.getLogoutURL())),\
                             "loginAsURL": self.getLoginAsURL() } )
    
    def _getNavigationDrawer(self):
        pars = {"target": self._target , "isModif" : True}
        return wcomponents.WNavigationDrawer( pars, bgColor = "white" )
        
    def _createSideMenu( self ):
        self._sideMenu = wcomponents.ManagementSideMenu()
        
        viewSection = wcomponents.SideMenuSection()
        
        self._viewMenuItem = wcomponents.SideMenuItem(_("View category"),
            urlHandlers.UHCategoryDisplay.getURL( self._target ))
        viewSection.addItem( self._viewMenuItem)
        
        self._sideMenu.addSection(viewSection)
        

        mainSection = wcomponents.SideMenuSection()
        
        self._generalSettingsMenuItem = wcomponents.SideMenuItem(_("General settings"),
            urlHandlers.UHCategoryModification.getURL( self._target ))
        mainSection.addItem( self._generalSettingsMenuItem)
        
        self._filesMenuItem = wcomponents.SideMenuItem(_("Files"),
            urlHandlers.UHCategModifFiles.getURL(self._target ))
        mainSection.addItem( self._filesMenuItem)

        self._ACMenuItem = wcomponents.SideMenuItem(_("Protection"),
            urlHandlers.UHCategModifAC.getURL( self._target ))
        mainSection.addItem( self._ACMenuItem)

        self._toolsMenuItem = wcomponents.SideMenuItem(_("Tools"),
            urlHandlers.UHCategModifTools.getURL( self._target ))
        mainSection.addItem( self._toolsMenuItem)
        
        self._tasksMenuItem = wcomponents.SideMenuItem(_("Tasks"),
            urlHandlers.UHCategModifTasks.getURL( self._target ))
        mainSection.addItem( self._tasksMenuItem)
        if not self._target.tasksAllowed() :
            self._tasksMenuItem.setVisible(False)

        self._sideMenu.addSection(mainSection)

    def _createTabCtrl( self ):
        pass

    def _setActiveTab( self ):
        pass
        
    def _setActiveSideMenuItem( self ):
        pass
    
    def _getBody( self, params ):
        self._createSideMenu()
        self._setActiveSideMenuItem()
        
        self._createTabCtrl()
        self._setActiveTab()

        sideMenu = self._sideMenu.getHTML()

        frame = WCategoryModifFrame()
        p = { "category": self._target,
              "body": self._getPageContent( params ),
              "sideMenu": self._sideMenu.getHTML() }
        
        return frame.getHTML( p )

    def _getTabContent( self, params ):
        return "nothing"
    
    def _getPageContent( self, params ):
        return "nothing"

    def _getSiteArea(self):
        return "ModificationArea"


class WCategoryModifFrame(wcomponents.WTemplated):
    
    def __init__( self ):
        pass

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        return vars

class WPCategModifMain( WPCategoryModifBase ):
    
    def _setActiveSideMenuItem( self ):
        self._generalSettingsMenuItem.setActive()

    
class WCategModifMain(wcomponents.WTemplated):
    
    def __init__( self, category ):
        self._categ = category

    def __getSubCategoryItems( self, sl, modifURLGen ):
        temp = []
        for categ in sl:
            id = categ.getId()
            selbox = """<select name="newpos%s" onChange="this.form.oldpos.value='%s';this.form.submit();">""" % (sl.index(categ),sl.index(categ))
            for i in range (1,len(sl)+1):
                if i==sl.index(categ)+1:
                    selbox += "<option selected value='%s'>%s" % (i-1,i)
                else:
                    selbox += "<option value='%s'>%s" % (i-1,i)
            selbox += """
                </select>"""
            temp.append("""
                <tr>
                    <td>
                        <input type="checkbox" name="selectedCateg" value="%s">
                        %s
                        &nbsp;<a href="%s">%s</a>
                    </td>
                </tr>"""%(id, selbox,modifURLGen( categ ), categ.getName().strip() or "[no title]"))
        html = """
                <input type="hidden" name="oldpos">
                <table align="center">%s
                </table>"""%"".join( temp )
        return html
    
    def __getConferenceItems( self, cl, modifURLGen, modifURLOpen ):
        temp = []
        for conf in cl:
            if conf.isClosed():
                textopen = _(""" <b>[ <a href="%s"> _("re-open event")</a> ]</b>""") %  modifURLOpen(conf)
            else:
                textopen = ""
            temp.append("""
                <tr>
                    <td width="3%%">
                        <input type="checkbox" name="selectedConf" value="%s">
                    </td>
                    <td align="center" width="17%%">%s</td>
                    <td align="center" width="17%%">%s</td>
                    <td width="100%%"><a href="%s">%s</a>%s</td>
                </tr>"""%(conf.getId(), conf.getAdjustedStartDate().date(), conf.getAdjustedEndDate().date(),modifURLGen(conf), conf.getTitle(), textopen))
        html = _("""<table align="left" width="100%%">
                <tr>
                    <td width="3%%" nowrap><img src="%s" border="0" alt="Select all" onclick="javascript:selectAll()"><img src="%s" border="0" alt="Deselect all" onclick="javascript:deselectAll()"></td>
                    <td align="center" width="17%%" class="titleCellFormat" style="border-right:5px solid #FFFFFF; border-bottom: 1px solid #FFFFFF;"> _("Start date")</td>
                    <td align="center" width="17%%" class="titleCellFormat" style="border-right:5px solid #FFFFFF; border-bottom: 1px solid #FFFFFF;"> _("End date")</td>
                    <td width="100%%" class="titleCellFormat" style="border-right:5px solid #FFFFFF; border-bottom: 1px solid #FFFFFF;"> _("Conference title")</td>
                </tr>
        %s</table>""")%(Config.getInstance().getSystemIconURL("checkAll"), Config.getInstance().getSystemIconURL("uncheckAll"), "".join( temp ))
        return html

    def getVars( self ):
        
        vars = wcomponents.WTemplated.getVars( self )
        vars["locator"] = self._categ.getLocator().getWebForm()
        vars["name"] = self._categ.getName()
        
        vars["description"] = self._categ.getDescription()
        
        if self._categ.getIcon() is not None:
            vars["icon"] = """<img src="%s" width="16" height="16" alt="category">"""%urlHandlers.UHCategoryIcon.getURL( self._categ)
        else:
            vars["icon"] = "None"
        vars["dataModifButton"] = ""
        if not self._categ.isRoot():
            vars["dataModifButton"] = _("""<input type="submit" class="btn" value="_("modify")">""")
        vars["removeItemsURL"] = vars["actionSubCategsURL"]
        if not self._categ.getSubCategoryList():
             vars["removeItemsURL"] = vars["actionConferencesURL"]
             vars["items"] = self.__getConferenceItems( self._categ.getConferenceList(True,3), vars["confModifyURLGen"],  vars["confModifyURLOpen"])
        else:
            vars["items"] = self.__getSubCategoryItems( self._categ.getSubCategoryList(), vars["categModifyURLGen"] )
        styleMgr = info.HelperMaKaCInfo.getMaKaCInfoInstance().getStyleManager()
        vars["defaultMeetingStyle"] = styleMgr.getStylesheetName(self._categ.getDefaultStyle("meeting"))
        vars["defaultLectureStyle"] = styleMgr.getStylesheetName(self._categ.getDefaultStyle("simple_event"))

##        vars["defaultVisibility"] = self._categ.getVisibility() 
        vars["defaultTimezone"] = self._categ.getTimezone()
        visibility = self._categ.getVisibility()
        categpath = self._categ.getCategoryPath()
        categpath.reverse()
        if visibility > len(categpath):
            vars["defaultVisibility"] = _("Everywhere")
        elif visibility == 0:
            vars["defaultVisibility"] = _("Nowhere")
        else:
            categId = categpath[visibility-1]
            cat = conference.CategoryManager().getById(categId)
            vars["defaultVisibility"] = cat.getName()

###################################################################################################
## TODO: this code belongs to the TASKS MODULE. We should fix it or remove it.        
        vars["enablePic"]=quoteattr(str(Config.getInstance().getSystemIconURL( "enabledSection" )))
        vars["disablePic"]=quoteattr(str(Config.getInstance().getSystemIconURL( "disabledSection" )))
        enabledText = _("Click to disable")
        disabledText = _("Click to enable")
        
        url = urlHandlers.UHCategoryTasksOption.getURL( self._categ )
                
        comment = ""
        if (self._categ.hasSubcategories()):
            icon=vars["disablePic"]
            textIcon = disabledText    
            comment = _("""<b>&nbsp;&nbsp;[ _("Category contains subcategories - this module cannot be enabled")]</b>""")
            url = ""
        elif self._categ.tasksAllowed():
            icon=vars["enablePic"]
            textIcon=enabledText
            if len(self._categ.getTaskList()) > 0 :
                comment = _("""<b>&nbsp;&nbsp;[_("Task list is not empty - this module cannot be disabled")]</b>""")
                url = ""
        else:
            icon=vars["disablePic"]
            textIcon=disabledText     
        tasksManagement = """
        <tr>
            <td>
                <a href=%s><img src=%s alt="%s" class="imglink"></a>&nbsp;<a href=%s>%s</a>%s
            </td>
        </tr>"""%(url,icon,textIcon,url, _("Tasks List"),comment)
        vars["tasksManagement"] = tasksManagement
###################################################################################################
        return vars


class WPCategoryModification( WPCategModifMain ):
    
    def _getPageContent( self, params ):
        wc = WCategModifMain( self._target )
        pars = { \
"dataModificationURL": urlHandlers.UHCategoryDataModif.getURL( self._target ), \
"addSubCategoryURL": urlHandlers.UHCategoryCreation.getURL(), \
"addConferenceURL": urlHandlers.UHConferenceCreation.getURL( self._target ), \
"confModifyURLGen": urlHandlers.UHConferenceModification.getURL, \
"confModifyURLOpen": urlHandlers.UHConferenceOpen.getURL, \
"categModifyURLGen": urlHandlers.UHCategoryModification.getURL, \
"actionSubCategsURL": urlHandlers.UHCategoryActionSubCategs.getURL(), \
"actionConferencesURL": urlHandlers.UHCategoryActionConferences.getURL()}
        return wc.getHTML( pars )        


class WCategoryDataModification(wcomponents.WTemplated):
    
    def __init__( self, category ):
        self._categ = category

    def _getVisibilityHTML(self):
        visibility = self._categ.getVisibility()
        topcat = self._categ
        level = 0
        selected = ""
        if visibility == 0:
            selected = "selected"
        vis = [ _("""<option value="0" %s> _("Nowhere")</option>""") % selected]
        while topcat:
            level += 1
            selected = ""
            if level == visibility:
                selected = "selected"
            if topcat.getId() != "0":
                from MaKaC.common.TemplateExec import truncateTitle 
                vis.append("""<option value="%s" %s>%s</option>""" % (level, selected, truncateTitle(topcat.getName(), 70)))
            topcat = topcat.getOwner()
        selected = ""
        if visibility > level:
            selected = "selected"
        vis.append( _("""<option value="999" %s> _("Everywhere")</option>""") % selected)
        vis.reverse()
        return "".join(vis)
        
    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars["locator"] = self._categ.getLocator().getWebForm()
        vars["name"] = self._categ.getName()
        vars["description"] = self._categ.getDescription()
        vars["visibility"] = self._getVisibilityHTML()
        vars["timezoneOptions"] = TimezoneRegistry.getShortSelectItemsHTML(self._categ.getTimezone())
        if self._categ.getIcon() is not None:
            vars["icon"] = """<img src="%s" width="16" height="16" alt="category">"""%urlHandlers.UHCategoryIcon.getURL( self._categ)
        else:
            vars["icon"] = "None"
        for type in [ "simple_event", "meeting" ]:
            styleMgr = info.HelperMaKaCInfo.getMaKaCInfoInstance().getStyleManager()
            stylesheets = styleMgr.getStylesheetListForEventType(type)
            styleoptions = ""
            for stylesheet in stylesheets:
                defStyle = self._categ.getDefaultStyle(type)
                if defStyle == "":
                    defStyle = styleMgr.getDefaultStylesheetForEventType(type)
                if stylesheet == defStyle:
                    selected = "selected"
                else:
                    selected = ""
                styleoptions += "<option value=\"%s\" %s>%s</option>" % (stylesheet,selected,styleMgr.getStylesheetName(stylesheet))
            vars["%sStyleOptions" % type] = styleoptions
        
            
        return vars


class WPCategoryDataModification( WPCategModifMain ):
    
    def _getPageContent( self, params ):
        wc = WCategoryDataModification( self._target )
        pars = {"postURL": urlHandlers.UHCategoryPerformModification.getURL() }
        return wc.getHTML( pars )


class WCategoryCreation(wcomponents.WTemplated):
    
    def __init__( self, target ):
        self.__target = target

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars["locator"] = self.__target.getLocator().getWebForm()
        for type in [ "simple_event", "meeting" ]:
            styleMgr = info.HelperMaKaCInfo.getMaKaCInfoInstance().getStyleManager()
            stylesheets = styleMgr.getStylesheetListForEventType(type)
            styleoptions = ""
            for stylesheet in stylesheets:
                defStyle = self.__target.getDefaultStyle(type)
                if defStyle == "":
                    defStyle = styleMgr.getDefaultStylesheetForEventType(type)
                if stylesheet == defStyle:
                    selected = "selected"
                else:
                    selected = ""
                styleoptions += "<option value=\"%s\" %s>%s</option>" % (stylesheet,selected,styleMgr.getStylesheetName(stylesheet))
            vars["%sStyleOptions" % type] = styleoptions
        minfo = info.HelperMaKaCInfo.getMaKaCInfoInstance()
        try:
           default_tz = minfo.getTimezone()
        except:
           default_tz = 'UTC'
        vars["timezoneOptions"] = TimezoneRegistry.getShortSelectItemsHTML(default_tz)
        return vars


class WPCategoryCreation( WPCategModifMain ):
    
    def _getPageContent( self, params ):
        wc = WCategoryCreation( self._target )
        pars = { "categDisplayURLGen": urlHandlers.UHCategoryDisplay.getURL, \
                "postURL": urlHandlers.UHCategoryPerformCreation.getURL() }
        return wc.getHTML( pars )


class WCategoryDeletion(object):
    
    def __init__( self, categoryList ):
        self._categList = categoryList

    def getHTML( self, actionURL ):
        l = []
        for categ in self._categList:
            l.append("""<li><i>%s</i></li>"""%categ.getName())
        msg = _("""
        <font size="+2"> _("Are you sure that you want to DELETE the following categories"):<ul>%s</ul>?</font><br>( _("Note that ALL the existing sub-categories below will also be deleted"))
              """)%("".join(l))
        wc = wcomponents.WConfirmation()
        categIdList = []
        for categ in self._categList:
            categIdList.append( categ.getId() )
        return wc.getHTML( msg, actionURL, {"selectedCateg": categIdList}, \
                                            confirmButtonCaption= _("Yes"), \
                                            cancelButtonCaption= _("No") )


class WConferenceDeletion(object):
    
    def __init__( self, conferenceList ):
        self._confList = conferenceList

    def getHTML( self, actionURL ):
        l = []
        for event in self._confList:
            l.append("""<li><i>%s</i></li>"""%event.getTitle())
        msg = _("""<font size="+2">Are you sure that you want to <font color="red"><b>DELETE</b></font> the following events:<ul>%s</ul>?</font><br>(Note that ALL the existing sub-categories below will also be deleted)""")%("".join(l))
        wc = wcomponents.WConfirmation()
        eventIdList = []
        for event in self._confList:
            eventIdList.append( event.getId() )
        return wc.getHTML( msg, actionURL, {"selectedConf": eventIdList}, \
                                            confirmButtonCaption= _("Yes"), \
                                            cancelButtonCaption= _("No") )


class WPSubCategoryDeletion( WPCategModifMain ):
    
    def _getPageContent( self, params ):
        selCategs = params["subCategs"]
        wc = WCategoryDeletion( selCategs )
        return wc.getHTML( urlHandlers.UHCategoryActionSubCategs.getURL( self._target ) )

class WPConferenceDeletion(WPCategModifMain ):

    def _getPageContent( self, params ):
        #raise '%s'%params
        selConfs = params["events"]
        wc = WConferenceDeletion( selConfs )
        return wc.getHTML( urlHandlers.UHCategoryActionConferences.getURL( self._target ) )


class WItemReallocation( wcomponents.WTemplated ):  
    
    def __init__( self, itemList ):
        self._itemList = itemList

    def getHTML( self, selectTree, params):
        self._sTree = selectTree
        return wcomponents.WTemplated.getHTML( self, params )
    
    def _getItemDescription( self, item ):
        return ""

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        l = []
        for item in self._itemList:
            l.append("<li><b>%s</b>"%self._getItemDescription(item))
        vars["selectedItems"] = "".join(l)
        vars["categTree"] = self._sTree.getHTML() 
        return vars


class WCategoryReallocation( WItemReallocation ):  
    
    def _getItemDescription( self, item ):
        return item.getName()


class WConferenceReallocation( WItemReallocation ):  
    
    def _getItemDescription( self, item ):
        return item.getTitle()


class CategSelectTree:
    
    def __init__( self, aw, excludedCat, expandedCat, \
                        selectURLGen, expandURLGen, movingConference = 0 ):
        self._aw = aw
        self._excludedCategs = excludedCat
        self._expandedCategs = expandedCat
        self._selectURLGen = selectURLGen
        self._expandURLGen = expandURLGen
        self._movingConference = movingConference

    def _getItem( self, categ, level=0 ):
        if not categ.canView( self._aw ):
            return ""
        html = ""
        for i in range(level):
            html = "%s&nbsp;&nbsp;&nbsp;"%html
        cfg = Config.getInstance()
        if categ in self._excludedCategs:
            return """%s<img src="%s" border="0" alt=""> %s"""%(html, cfg.getSystemIconURL("itemCollapsed"), categ.getName())
        if (self._movingConference) and categ.getSubCategoryList():
            title = """%s"""%categ.getName()
        else:
            title = """<a href="%s">%s</a>"""%(self._selectURLGen( categ ), \
                                                categ.getName())
        if categ in self._expandedCategs:
            ex = copy( self._expandedCategs )
            ex.remove( categ )
            html = """%s<a href="%s"><img src="%s" border="0" alt=""></a> %s"""%(html, self._expandURLGen( ex ), cfg.getSystemIconURL("itemExploded"), title)
            for subcat in categ.getSubCategoryList():
                html = "%s<br>%s"%(html, self._getItem(subcat, level+1) )
        else:
            html = """%s<a href="%s"><img src="%s" border="0" alt=""></a> %s"""%(html, self._expandURLGen( self._expandedCategs+[categ] ), cfg.getSystemIconURL("itemCollapsed"), title)
        return html
        
    def getHTML( self ):
        cm = conference.CategoryManager()
        return self._getItem( cm.getRoot() )


class WPCategoryReallocation( WPCategModifMain ):
    
    def _getReAllocateCategsURL( self, destination ):
        url = urlHandlers.UHCategoryActionSubCategs.getURL( destination )
        selectedCategs = []
        for c in self._categs:
            selectedCategs.append( c.getId() )
        url.addParam( "selectedCateg", selectedCategs )
        url.addParam( "confirm", "" )
        url.addParam( "reallocate", "" )
        return url
    
    def _getCategExpandCategURL( self, expandedCategs ):
        selected = []
        for c in self._categs:
            selected.append( c.getId() )
        expanded = []
        for c in expandedCategs:
            expanded.append( c.getId() )
        url = urlHandlers.UHCategoryActionSubCategs.getURL( self._target )
        url.addParam( "selectedCateg", selected )
        url.addParam( "ex", expanded )
        url.addParam( "reallocate", "" )
        return url
    
    def _getExpandedCategs( self, params ):
        exIdList = params.get("ex", [])
        if not isinstance( exIdList, list ):
            exIdList = [ exIdList ]
        expanded = []
        cm = conference.CategoryManager()
        for categId in exIdList:
            expanded.append( cm.getById( categId ) )
        return expanded

    def _getPageContent( self, params ):
        self._categs = params["subCategs"]
        expanded = self._getExpandedCategs( params )
        pars = {"cancelURL": urlHandlers.UHCategoryModification.getURL( self._target ) }
        tree = CategSelectTree( self._getAW(), self._categs, \
                                            expanded, \
                                            self._getReAllocateCategsURL, \
                                            self._getCategExpandCategURL )
        wc = WCategoryReallocation( self._categs )
        return wc.getHTML( tree, pars )


class WPConferenceReallocation( WPCategModifMain ):
    
    def _getReAllocateConfsURL( self, destination ):
        url = urlHandlers.UHCategoryActionConferences.getURL( destination )
        url.addParam( "srcCategId", self._target.getId() )
        url.addParam( "selectedConf", self._confIds)
        url.addParam( "confirm", "" )
        url.addParam( "reallocate", "" )
        return url
    
    def _getExpandCategURL( self, expandedCategs ):
        expanded = []
        for c in expandedCategs:
            expanded.append( c.getId() )
        url = urlHandlers.UHCategoryActionConferences.getURL( self._target )
        url.addParam( "ex", expanded )
        url.addParam( "reallocate", "" )
        url.addParam( "selectedConf", self._confIds )
        return url
    
    def _getExpandedCategs( self, params ):
        exIdList = params.get("ex", [])
        if not isinstance( exIdList, list ):
            exIdList = [ exIdList ]
        expanded = []
        cm = conference.CategoryManager()
        for categId in exIdList:
            expanded.append( cm.getById( categId ) )
        return expanded

    def _getPageContent( self, params ):
        self._confs = params["confs"]
        self._confIds = []
        for c in self._confs:
            self._confIds.append( c.getId() )
        expanded = self._getExpandedCategs( params )
        pars = {"cancelURL": urlHandlers.UHCategoryModification.getURL( self._target ) }
        tree = CategSelectTree( self._getAW(), [], \
                                            expanded, \
                                            self._getReAllocateConfsURL, \
                                            self._getExpandCategURL, 1 )
        wc = WConferenceReallocation( self._confs )
        return wc.getHTML( tree, pars )


class WCategModifAC(wcomponents.WTemplated):
    
    def __init__( self, category ):
        self._categ = category

    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars["modifyControlFrame"] = wcomponents.WModificationControlFrame().getHTML(\
                                                    self._categ,\
                                                    vars["addManagersURL"],\
                                                    vars["removeManagersURL"] )
        vars["accessControlFrame"] = wcomponents.WAccessControlFrame().getHTML(\
                                                    self._categ,\
                                                    vars["setVisibilityURL"],\
                                                    vars["addAllowedURL"],\
                                                    vars["removeAllowedURL"] )
        if not self._categ.isProtected():
            df =  wcomponents.WDomainControlFrame( self._categ )
            vars["accessControlFrame"] += "<br>%s"%df.getHTML( \
                                                    vars["addDomainURL"], \
                                                    vars["removeDomainURL"] )
        vars["confCreationControlFrame"] = ""
        if not self._categ.getSubCategoryList():
            frame = wcomponents.WConfCreationControlFrame( self._categ )
            p = { "setStatusURL": vars["setConferenceCreationControlURL"], \
                  "addCreatorsURL": vars["addConferenceCreatorsURL"], \
                  "removeCreatorsURL": vars["removeConfenceCreatorsURL"] }
            vars["confCreationControlFrame"] = frame.getHTML(p)
        return vars
    
class WPCategModifAC( WPCategoryModifBase ):
    
    def _setActiveSideMenuItem( self ):
        self._ACMenuItem.setActive()
    
    def _getPageContent( self, params ):
        wc = WCategModifAC( self._target )
        pars = { \
"addManagersURL": urlHandlers.UHCategorySelectManagers.getURL(), \
"removeManagersURL": urlHandlers.UHCategoryRemoveManagers.getURL(), \
"setVisibilityURL": urlHandlers.UHCategorySetVisibility.getURL(), \
"addAllowedURL": urlHandlers.UHCategorySelectAllowed.getURL(), \
"removeAllowedURL": urlHandlers.UHCategoryRemoveAllowed.getURL(), \
"addDomainURL": urlHandlers.UHCategoryAddDomain.getURL(), \
"removeDomainURL": urlHandlers.UHCategoryRemoveDomain.getURL(),\
"setConferenceCreationControlURL": urlHandlers.UHCategorySetConfCreationControl.getURL() , \
"addConferenceCreatorsURL": urlHandlers.UHCategorySelectConfCreators.getURL(),\
"removeConfenceCreatorsURL": urlHandlers.UHCategoryRemoveConfCreators.getURL() }
        return wc.getHTML( pars )        


class WPCategorySelectManagers( WPCategModifAC ):
    
    def _getPageContent( self, params ):
        searchExt = params.get("searchExt","")
        if searchExt != "":
            searchLocal = False
        else:
            searchLocal = True
        wc = wcomponents.WPrincipalSelection( urlHandlers.UHCategorySelectManagers.getURL(),forceWithoutExtAuth=searchLocal )
        params["addURL"] = urlHandlers.UHCategoryAddManagers.getURL()
        return wc.getHTML( params )


class WPCategorySelectAllowed( WPCategModifAC ):
    
    def _getPageContent( self, params ):
        searchExt = params.get("searchExt","")
        if searchExt != "":
            searchLocal = False
        else:
            searchLocal = True
        wc = wcomponents.WPrincipalSelection( urlHandlers.UHCategorySelectAllowed.getURL(),forceWithoutExtAuth=searchLocal )
        params["addURL"] = urlHandlers.UHCategoryAddAllowed.getURL()
        return wc.getHTML( params )


class WPCategorySelectConfCreators( WPCategModifAC ):
    
    def _getPageContent( self, params ):
        searchExt = params.get("searchExt","")
        if searchExt != "":
            searchLocal = False
        else:
            searchLocal = True
        wc = wcomponents.WPrincipalSelection( urlHandlers.UHCategorySelectConfCreators.getURL(),forceWithoutExtAuth=searchLocal )
        params["addURL"] = urlHandlers.UHCategoryAddConfCreators.getURL()
        return wc.getHTML( params )

#---------------------------------------------------------------------------------

class WCategModifTools(wcomponents.WTemplated):
    
    def __init__( self, category ):
        self._categ = category
    
    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        vars["deleteButton"] = ""
        vars["id"] = self._categ.getId()
        if not self._categ.isRoot():
            vars["deleteButton"] = _("""<input type="submit" class="btn" value="_("delete this category")">""")
        vars["clearCache"] = ""
        if info.HelperMaKaCInfo.getMaKaCInfoInstance().isCacheActive():
            vars["clearCache"] = _("""<form action="%s" method="POST"><input type="submit" class="btn" value="_("clear category cache")"></form>""") % urlHandlers.UHCategoryClearCache.getURL(self._categ)
            if len(self._categ.getConferenceList()):
                vars["clearCache"] += _("""<form action="%s" method="POST"><input type="submit" class="btn" value="_("clear conference caches")"></form>""") % urlHandlers.UHCategoryClearConferenceCaches.getURL(self._categ)    
        return vars


class WPCategModifTools( WPCategoryModifBase ):
    
    def _setActiveSideMenuItem( self ):
        self._toolsMenuItem.setActive()
    
    def _getPageContent( self, params ):
        wc = WCategModifTools( self._target )
        pars = { \
"deleteCategoryURL": urlHandlers.UHCategoryDeletion.getURL(self._target) }
        return wc.getHTML( pars )        


class WPCategoryDeletion( WPCategModifTools ):
    
    def _getPageContent( self, params ):
        wc = WCategoryDeletion( [self._target] )
        return wc.getHTML( urlHandlers.UHCategoryDeletion.getURL( self._target ) )

#---------------------------------------------------------------------------------

class WCategModifTasks(wcomponents.WTemplated):
    
    def __init__( self, category ):
        self._categ = category
    
    def getVars( self ):
        vars = wcomponents.WTemplated.getVars( self )
        if self._categ.tasksAllowed() :
            vars["tasksAllowed"] = _("Adding tasks is allowed")
        else :
            vars["tasksAllowed"] = _("Adding tasks IS NOT allowed")
        vars["id"] = self._categ.getId()
        vars["taskAction"] = urlHandlers.UHCategModifTasksAction.getURL(self._categ)
        vars["locator"] = ""
        
        if self._categ.tasksPublic() :
            vars["accessVisibility"] = _("PUBLIC")
            oppVisibility = _("PRIVATE")
        else :
            vars["accessVisibility"] = _("PRIVATE")
            oppVisibility = _("PUBLIC")
        vars["changeAccessVisibility"] = _("""( _("make it") <input type="submit" class="btn" name="accessVisibility" value="%s">)""")%oppVisibility
        
        if not self._categ.tasksPublic() :
            vars["commentVisibility"] = _("PRIVATE")
            vars["changeCommentVisibility"] = """"""
        else :
            if self._categ.tasksCommentPublic() :                
                vars["commentVisibility"] = _("PUBLIC")
                oppVisibility = _("PRIVATE")
            else :
                vars["commentVisibility"] = _("PRIVATE")
                oppVisibility = _("PUBLIC")
            vars["changeCommentVisibility"] = _("""( _("make it") <input type="submit" class="btn" name="commentVisibility" value="%s">)""")%oppVisibility
        
                
        vars["managerList"] = self._getPersonList("manager") 
        vars["commentList"] = self._getPersonList("commentator") 
        vars["accessList"] = self._getPersonList("access") 
                        
        vars["accessOptions"] = self._getAccessOptions()
        vars["commentOptions"] = self._getCommentOptions()
        vars["managerOptions"] = self._getManagerOptions()
        
            
        return vars

    def _getAccessOptions(self, names=[]):
        html = []
        if len(names) == 0 :
            html.append("""<option value=""> </option>""")
        for event in self._categ.getConferenceList() :
            index = 0
            for chair in event.getChairList() :
                text = """<option value="h%s-%s">%s</option>"""%(event.getId(),index,chair.getFullName())
                index = index + 1
                if not (chair.getFullName() in names) :
                    html.append(text)
                    names.append(chair.getFullName())
            index = 0
            for manager in event.getManagerList() :
                text = """<option value="m%s-%s">%s</option>"""%(event.getId(),index,manager.getFullName())
                index = index + 1
                if not (manager.getFullName() in names) :
                    html.append(text)
                    names.append(manager.getFullName())
            index = 0
            for participant in event.getParticipation().getParticipantList():
                text = """<option value="p%s-%s">%s</option>"""%(event.getId(),index,participant.getFullName())
                index = index + 1
                if not (participant.getFullName() in names) :
                    html.append(text)
                    names.append(participant.getFullName())                    
        return """
                """.join(html)
        
    def _getCommentOptions(self, names=[]):
        html = []
        if len(names) == 0 :
            html.append("""<option value=""> </option>""")
        index = 0
        for a in self._categ.getTasksAccessList() :
            text = """<option value="a%s">%s</option>"""%(index,a.getFullName())
            index = index + 1
            if not (a.getFullName() in names) :
                html.append(text)
                names.append(a.getFullName())
        list = """
        """.join(html)
        
        return list + """
        """+self._getAccessOptions(names)
        
    def _getManagerOptions(self):
        html = []
        names = []
        html.append("""<option value=""> </option>""")
        index = 0
        for c in self._categ.getTasksCommentatorList() :
            text = """<option value="c%s">%s</option>"""%(index,c.getFullName())
            index = index + 1
            if not (c.getFullName() in names) :
                html.append(text)
                names.append(c.getFullName())                
        list = """
        """.join(html)
        
        return list + """
        """+self._getCommentOptions(names)


    def _getPersonList(self, personType): 
        html = []
        index = 0
        if personType == "access" :
            personList = self._categ.getTasksAccessList()
        elif personType == "manager" :
            personList = self._categ.getTasksManagerList()
        elif personType == "comentator" :
            personList = self._categ.getTasksCommentatorList() 
        else :
            return ""
        
        for a in personList :
            line = """
            <tr>
                <td><input type="checkbox" name="%s" value="%s"></td>
                <td>%s</td>
            </tr>
            """%(personType, index, a.getFullName())
            index = index + 1
            html.append(line)
        
        list = """
        """.join(html)
        out = """
       <table>
           %s
       </table>"""%list        
        return out

class WPCategModifTasks( WPCategoryModifBase ):
    
    def _setActiveSideMenuItem( self ):
        self._tasksMenuItem.setActive()
    
    def _getPageContent( self, params ):
        wc = WCategModifTasks( self._target )
        pars = { \
"deleteCategoryURL": urlHandlers.UHCategoryDeletion.getURL(self._target) }
        
        return wc.getHTML( pars )        

class WPCategoryModifExistingMaterials( WPCategoryModifBase ):
    
    def getJSFiles(self):
        return WPCategoryModifBase.getJSFiles(self) + \
               self._includeJSPackage('Management') + \
               self._includeJSPackage('MaterialEditor')

    def _getPageContent( self, pars ):
        wc=wcomponents.WShowExistingMaterial(self._target)
        return wc.getHTML( pars )
    
    def _setActiveSideMenuItem( self ):
        self._filesMenuItem.setActive()   

