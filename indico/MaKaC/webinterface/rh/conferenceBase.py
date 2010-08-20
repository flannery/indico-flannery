# -*- coding: utf-8 -*-
##
## $Id: conferenceBase.py,v 1.40 2009/05/27 10:05:40 pferreir Exp $
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

import tempfile
import os
import shutil
import stat
from copy import copy
import MaKaC.webinterface.locators as locators
import MaKaC.webinterface.webFactoryRegistry as webFactoryRegistry
import MaKaC.webinterface.urlHandlers as urlHandlers
from MaKaC.webinterface.rh.base import RH
from MaKaC.errors import MaKaCError
from MaKaC.common.Configuration import Config
from MaKaC.conference import LocalFile,Material,Link,Category,Conference
import MaKaC.webinterface.materialFactories as materialFactories
from MaKaC.export import fileConverter
from MaKaC.conference import Conference,Session,Contribution,SubContribution
from MaKaC.i18n import _

from MaKaC.common.logger import Logger

class RHCustomizable( RH ):

    def __init__( self, req ):
        RH.__init__( self, req )
        self._wf = ""

    def getWebFactory( self ):
        if self._wf == "":
           wr = webFactoryRegistry.WebFactoryRegistry()
           self._wf = wr.getFactory( self._conf )
        return self._wf


class RHConferenceSite( RHCustomizable ):

    def _setMenuStatus(self,params):
        if params.has_key("menuStatus"):
            self._getSession().setVar("menuStatus",params["menuStatus"])
 #       wr = webFactoryRegistry.WebFactoryRegistry()
 #       self._wf = wr.getFactory( self._conf )
 #       if self._wf is not None:
 #           self._getSession().setVar("menuStatus","close")

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setConference( params )
        self._conf = self._target = l.getObject()
        self._setMenuStatus(params)

    def _getLoginURL( self ):
        #url = self.getCurrentURL()
        url = self.getRequestURL()
        if url == "":
            url = urlHandlers.UHConferenceDisplay.getURL( self._conf )
        wr = webFactoryRegistry.WebFactoryRegistry()
        self._wf = wr.getFactory( self._conf )
        if self._wf is not None:
            return urlHandlers.UHSignIn.getURL( url )
        else:
            return urlHandlers.UHConfSignIn.getURL( self._target, url )



class RHConferenceBase( RHConferenceSite ):
    pass


class RHSessionBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setSession( params )
        self._session = self._target = l.getObject()
        self._conf = self._session.getConference()
        self._setMenuStatus(params)

class RHSessionSlotBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setSlot( params )
        self._slot = self._target = l.getObject()
        self._session = self._slot.getSession()
        self._conf = self._session.getConference()
        self._setMenuStatus(params)


class RHContributionBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setContribution( params )
        self._contrib = self._target = l.getObject()
        self._conf = self._contrib.getConference()
        self._setMenuStatus(params)

class RHSubContributionBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setSubContribution( params )
        self._subContrib = self._target = l.getObject()
        self._contrib = self._subContrib.getParent()
        self._conf = self._contrib.getConference()
        self._setMenuStatus(params)


class RHMaterialBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setMaterial( params )
        self._material = self._target = l.getObject()
        if self._material is None:
            raise MaKaCError( _("The material you are trying to access does not exist or was removed"))
        self._conf = self._material.getConference()
        if self._conf == None:
            self._categ=self._material.getCategory()
        self._setMenuStatus(params)


class RHFileBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setResource( params )
        self._file = self._target = l.getObject()
        if not isinstance(self._file, LocalFile):
            raise MaKaCError("No file found, %s found instead"%type(self._file))
        self._conf = self._file.getConference()
        if self._conf == None:
            self._categ = self._file.getCategory()
        self._setMenuStatus(params)


class RHAlarmBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setAlarm( params )
        self._alarm = self._target = l.getObject()
        self._conf = self._alarm.getOwner().getConference()
        self._setMenuStatus(params)


class RHLinkBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setResource( params )
        self._link = self._target = l.getObject()
        self._conf = self._link.getConference()
        if self._conf == None:
            self._categ=self._link.getCategory()
        self._setMenuStatus(params)


class RHTrackBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setTrack( params )
        self._track = self._target = l.getObject()
        self._conf = self._track.getConference()
        self._subTrack = None
        if params.has_key("subTrackId"):
            self._subTrack = self._track.getSubTrackById(params["subTrackId"])
        self._setMenuStatus(params)


class RHAbstractBase( RHConferenceSite ):

    def _checkParams( self, params ):
        l = locators.WebLocator()
        l.setAbstract( params )
        self._abstract = self._target = l.getObject()
        if self._abstract is None:
            raise MaKaCError( _("The abstract you are trying to access does not exist"))
        self._conf = self._abstract.getOwner().getOwner()
        self._setMenuStatus(params)

class RHSubmitMaterialBase:


    def __init__(self, target, rh = None):
        self._target=target
        self._callerRH = rh
        self._repositoryId = None

    def _getNewTempFile( self ):
        cfg = Config.getInstance()
        tempPath = cfg.getUploadedFilesTempDir()
        tempFileName = tempfile.mkstemp( suffix="Indico.tmp", dir = tempPath )[1]
        return tempFileName

    #XXX: improve routine to avoid saving in temporary file
    def _saveFileToTemp( self, fd ):
        fileName = self._getNewTempFile()
        f = open( fileName, "wb" )
        f.write( fd.read() )
        f.close()
        return fileName

    def _checkParams(self,params):

        filesToDelete = []
        self._action = ""
        self._overwrite = False
        #if request has already been handled (DB conflict), then we keep the existing files list

        self._file = {}
        self._link = {}
        self._topdf=params.has_key("topdf")

        self._uploadType = params.get("uploadType","")
        self._materialId = params.get("materialId","")
        self._description = params.get("description","")
        self._statusSelection = int(params.get("statusSelection", 1))
        self._visibility = int(params.get("visibility", 0))
        self._password = params.get("password","")

        from MaKaC.services.interface.rpc import json
        self._userList = json.decode(params.get("userList", ""))

        if self._uploadType == "file":
            if type(params["file"]) != str and params["file"].filename.strip() != "":
                fDict = {}
                fDict["filePath"]=self._saveFileToTemp(params["file"].file)

                if self._callerRH != None:
                    self._callerRH._tempFilesToDelete.append(fDict["filePath"])

                fDict["fileName"]=params["file"].filename
                fDict["size"] = int(os.stat(fDict["filePath"])[stat.ST_SIZE])
                self._file = fDict

        elif self._uploadType == "link":
            link={}
            link["url"]=params.get("url","")
            link["matType"]=params.get("materialType","")
            self._link = link

    def _getErrorList(self):
        res=[]

        if self._uploadType == "file":
            if self._file == {}:
                res.append("""A file must be submitted.""")
            if hasattr(self._file, "filePath") and self._file["filePath"].strip()=="":
                res.append("""A valid file to be submitted must be specified.""")
            if hasattr(self._file, "size") and self._file["size"] < 10:
                res.append("""The file %s seems to be empty""" % self._file["fileName"])
        elif self._uploadType == "link":
            if self._link["url"].strip()=="":
                res.append("""A valid URL must be specified.""")

        if self._materialId=="":
            res.append("""A material ID must be selected.""")
        return res

    def _getMaterial(self, forceCreate = True):
        """
        Returns the Material object to which the resource is being added
        """

        registry = self._target.getMaterialRegistry()
        material = self._target.getMaterialById(self._materialId)

        if material:
            return material, False
        # there's a defined id (not new type)
        elif self._materialId:
            # get a material factory for it
            mf = registry.getById(self._materialId)
            # get a material from the material factory
            material = mf.get(self._target)

            # if the factory returns an empty material (doesn't exist)
            if material == None and forceCreate:
                # create one
                material = mf.create(self._target)
                newlyCreated = True
            else:
                newlyCreated = False

            return material, newlyCreated
        else:
            # else, something has gone wrong
            raise Exception("""A material ID must be specified.""")

    def _addMaterialType(self, text, user):

        from MaKaC.common.PickleJar import DictPickler

        Logger.get('requestHandler').debug('Adding %s - request %s ' % (self._uploadType, id(self._callerRH._req)))

        mat, newlyCreated = self._getMaterial()

        # if the material still doesn't exist, create it
        if newlyCreated:
            protectedAtResourceLevel = False
        else:
            protectedAtResourceLevel = True

        if self._uploadType in ['file','link']:
            if self._uploadType == "file":

                resource = LocalFile()
                resource.setFileName(self._file["fileName"])
                resource.setName(resource.getFileName())
                resource.setFilePath(self._file["filePath"])
                resource.setDescription(self._description)

                if not type(self._target) is Category:
                    self._target.getConference().getLogHandler().logAction({"subject":"Added file %s%s" % (self._file["fileName"],text)},"Files",user)
                # in case of db conflict we do not want to send the file to conversion again, nor re-store the file

            elif self._uploadType == "link":

                resource = Link()
                resource.setURL(self._link["url"])
                resource.setName(resource.getURL())
                resource.setDescription(self._description)

                if not type(self._target) is Category:
                    self._target.getConference().getLogHandler().logAction({"subject":"Added link %s%s" % (resource.getURL(),text)},"Files",user)

            status = "OK"
            info = resource
        else:
            status = "ERROR"
            info = "Unknown upload type"
            return mat, status, info

        mat.addResource(resource, forcedFileId=self._repositoryId)

        #apply conversion
        if self._topdf and fileConverter.CDSConvFileConverter.hasAvailableConversionsFor(os.path.splitext(resource.getFileName())[1].strip().lower()):
            Logger.get('conv').debug('Queueing %s for conversion' % resource.getFilePath())

            fileConverter.CDSConvFileConverter.convert(resource.getFilePath(), "pdf", mat)

        self._topdf = False

        # store the repo id, for files
        if isinstance(resource, LocalFile):
            self._repositoryId = resource.getRepositoryId()

        if protectedAtResourceLevel:
            protectedObject = resource
        else:
            protectedObject = mat
            mat.setHidden(self._visibility)
            mat.setAccessKey(self._password)

        protectedObject.setProtection(self._statusSelection)

        from MaKaC.user import AvatarHolder, GroupHolder

        for userElement in self._userList:
            if 'isGroup' in userElement and userElement['isGroup']:
                avatar = GroupHolder().getById(userElement['id'])
            else:
                avatar = AvatarHolder().getById(userElement['id'])
            protectedObject.grantAccess(avatar)

        return mat, status, DictPickler.pickle(info)

    def _process(self, rh, params):

        # We will need to pickle the data back into JSON

        errorList=[]
        user = rh.getAW().getUser()

        try:
            owner = self._target
            title = owner.getTitle()
            if type(owner) == Conference:
                ownerType = "event"
            elif type(owner) == Session:
                ownerType = "session"
            elif type(owner) == Contribution:
                ownerType = "contribution"
            elif type(owner) == SubContribution:
                ownerType = "subcontribution"
            else:
                ownerType = ""
            text = " in %s %s" % (ownerType,title)
        except:
            owner = None
            text = ""

        errorList=self._getErrorList()
        resource = None

        if len(errorList) > 0:
            status = "ERROR"
            info = errorList
        else:
            mat, status, info = self._addMaterialType(text, user)

            if status == "OK":
                info['material'] = mat.getId();

        # hackish, because of mime types. Konqueror, for instance, would assume text if there were no tags,
        # and would try to open it
        from MaKaC.services.interface.rpc import json
        return "<html><head></head><body>"+json.encode({'status': status, 'info': info})+"</body></html>"

