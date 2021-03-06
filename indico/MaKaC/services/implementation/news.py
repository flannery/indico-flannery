from MaKaC.services.implementation.base import ParameterManager,\
    TextModificationBase
from MaKaC.services.implementation.base import AdminService

from MaKaC.modules.base import ModulesHolder
from MaKaC.modules.news import NewsItem
from MaKaC.common.utils import formatDateTime
from MaKaC.services.interface.rpc.common import ServiceError
from MaKaC.common.PickleJar import DictPickler

class NewsRecentDays(TextModificationBase, AdminService):
    """ Set number of days that a news item is considered recent
    """
    def _handleSet(self):
        newDays = self._value
        try:
            newDays = int(self._value)
        except ValueError, e:
            raise ServiceError('ERR-NEWS0', 'Recent days value has to be an interger', e)

        newsModule = ModulesHolder().getById("news")
        newsModule.setRecentDays(newDays)

    def _handleGet(self):
        newsModule = ModulesHolder().getById("news")
        return newsModule.getRecentDays()

class NewsAdd(AdminService):

    def _checkParams(self):
        AdminService._checkParams(self)

        pm = ParameterManager(self._params)

        self._title = pm.extract("title", pType=str, allowEmpty=False)
        self._type = pm.extract("type", pType=str, allowEmpty=False)
        self._content = pm.extract("content", pType=str, allowEmpty=True)

    def _getAnswer(self):
        newsModule=ModulesHolder().getById("news")
        ni=NewsItem(self._title, self._content, self._type)
        newsModule.addNewsItem(ni)
        tz = self.getAW().getUser().getTimezone() #this is an admin service so user is always logged in (or _checkProtection detects it before)
        return DictPickler.pickle(ni, tz)

class NewsDelete(AdminService):

    def _checkParams(self):
        AdminService._checkParams(self)

        pm = ParameterManager(self._params)

        self._id = pm.extract("id", pType=str, allowEmpty=False)

    def _getAnswer(self):
        newsModule=ModulesHolder().getById("news")
        newsModule.removeNewsItem(self._id)

class NewsSave(AdminService):

    def _checkParams(self):
        AdminService._checkParams(self)

        pm = ParameterManager(self._params)

        self._id = pm.extract("id", pType=str, allowEmpty=False)
        self._title = pm.extract("title", pType=str, allowEmpty=False)
        self._type = pm.extract("type", pType=str, allowEmpty=False)
        self._content = pm.extract("content", pType=str, allowEmpty=True)

    def _getAnswer(self):
        newsModule=ModulesHolder().getById("news")
        item=newsModule.getNewsItemById(self._id)
        if item:
            item.setTitle(self._title)
            item.setType(self._type)
            item.setContent(self._content)
            tz = self.getAW().getUser().getTimezone() #this is an admin service so user is always logged in (or _checkProtection detects it before)
            return DictPickler.pickle(item, tz)
        else:
            raise Exception("News item does not exist")


methodMap = {
    "setRecentDays": NewsRecentDays,
    "add": NewsAdd,
    "delete": NewsDelete,
    "save": NewsSave
    }

