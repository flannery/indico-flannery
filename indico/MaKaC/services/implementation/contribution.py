from MaKaC.services.implementation.base import ProtectedModificationService
from MaKaC.services.implementation.base import ProtectedDisplayService
from MaKaC.services.implementation.base import ParameterManager
from MaKaC.services.implementation.roomBooking import GetBookingBase

from MaKaC.services.interface.rpc.common import ServiceError

from MaKaC.common.PickleJar import DictPickler

import MaKaC.conference as conference
from MaKaC.services.implementation.base import TextModificationBase
from MaKaC.services.implementation.base import HTMLModificationBase
from MaKaC.services.implementation.base import DateTimeModificationBase

class ContributionBase(object):

    def _checkParams( self ):        
        try:
            self._conf = conference.ConferenceHolder().getById(self._params["conference"]);
            if self._conf == None:
                raise Exception("Conference id not specified.")        
        except:           
            raise ServiceError("ERR-E4", "Invalid conference id.")

        try:
            self._target = self._contribution = self._conf.getContributionById(self._params["contribution"])
            if self._target == None:
                raise Exception("Contribution id not specified.")        
        except:           
            raise ServiceError("ERR-C0", "Invalid contribution id.")

        # create a parameter manager that checks the consistency of passed parameters
        self._pm = ParameterManager(self._params)

class ContributionDisplayBase(ProtectedDisplayService, ContributionBase):
    
    def _checkParams(self):
        ContributionBase._checkParams(self)
        ProtectedDisplayService._checkParams(self)

class ContributionModifBase(ContributionBase, ProtectedModificationService):
    
    def _checkProtection(self):
        if self._target.getSession() != None:
            if self._target.getSession().canCoordinate(self.getAW(), "modifContribs"):
                return
        ProtectedModificationService._checkProtection(self)
        
class ContributionTextModificationBase(TextModificationBase, ContributionBase):
    pass

class ContributionHTMLModificationBase(HTMLModificationBase, ContributionBase):
    pass

class ContributionDateTimeModificationBase (DateTimeModificationBase, ContributionBase):
    pass

class ContributionDeleteSubContribution(ContributionModifBase):
    def _checkParams(self):
        ContributionModifBase._checkParams(self)
        
        subcId = self._params.get('subContribution',None)
        
        self._subCont = self._target.getSubContributionById(subcId) 
            
        ProtectedModificationService._checkProtection(self)
    
    def _getAnswer(self):
        self._subCont.getOwner().removeSubContribution(self._subCont)

class ContributionAddSubContribution(ContributionModifBase):
    def _checkParams(self):
        ContributionModifBase._checkParams(self)
        
        # "presenters" and "keywords" are not required. they can be empty
        self._presenters = self._pm.extract("presenters", pType=list, allowEmpty=True)
        self._keywords = self._pm.extract("keywords", pType=list, allowEmpty=True)
        self._description = self._pm.extract("description", pType=str, allowEmpty=True, defaultValue="")
        
        # these are required        
        self._duration = self._pm.extract("duration", pType=int)
        self._title = self._pm.extract("title", pType=str)
        
    def __addPresenters(self, subcontrib):
        
        # add each presenter
        for presenterValues in self._presenters:
            
            # magically update a new ContributionParticipation with JSON data, using the DictPickler            
            presenter = conference.SubContribParticipation()
            DictPickler.update(presenter, presenterValues)

            subcontrib.newSpeaker(presenter)
        
    def _getAnswer(self):
        # create the sub contribution
        sc = self._target.newSubContribution()
        
        sc.setTitle( self._title )
        sc.setDescription( self._description )
        # separate the keywords using newlines
        sc.setKeywords('\n'.join(self._keywords))
        sc.setDuration( self._duration / 60, \
                         self._duration % 60 )   
                
        self.__addPresenters(sc)
        
        # log the event
        logInfo = sc.getLogInfo()
        logInfo["subject"] = "Create new subcontribution: %s"%sc.getTitle()
        self._target.getConference().getLogHandler().logAction(logInfo, "Timetable/SubContribution", self._getUser())

#TODO: this class is duplicated. check if the good one is the one before or this one!                
class ContributionDeleteSubContribution(ContributionModifBase):

    # contribution.deleteSubContribution

    _asyndicoDoc = {
        'summary':  'Deletes a subcontribution, given the conference, contribution and subcontribution IDs.',
        'params': [{'name': 'conference', 'type': 'str'},
                   {'name': 'contribution', 'type': 'str'},
                   {'name': 'subcontribution', 'type': 'str'}],
        'return': None
        }
    
    def _checkParams(self):
        ContributionModifBase._checkParams(self)
        
        subContId = self._pm.extract("subcontribution", pType=str, allowEmpty=False)

        self._subContribution = self._contribution.getSubContributionById(subContId)
        
    def _getAnswer(self):
        self._subContribution.getOwner().removeSubContribution(self._subContribution)

class ContributionGetBooking(ContributionDisplayBase, GetBookingBase):
    pass

methodMap = {
    "addSubContribution": ContributionAddSubContribution,
    "deleteSubContribution": ContributionDeleteSubContribution,
    "getBooking": ContributionGetBooking
}
