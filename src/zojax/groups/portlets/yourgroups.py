##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope.component import getUtility
from zojax.catalog.interfaces import ICatalog


class YourGroupsPortlet(object):

    groups = None

    def getGroups(self):
        if self.groups is not None:
            return self.groups

        results = getUtility(ICatalog).searchResults(
            type = {'any_of': ('content.group',)},
            members = {'any_of': (self.request.principal.id,)})

        groups = []
        for group in results:
            groups.append(
                (group.title,
                 {'name': group.__name__,
                  'title': group.title,
                  'description': group.description}))

        groups.sort()
        self.groups = [info for t, info in groups]
        return groups

    def isAvailable(self):
        groups = self.getGroups()
        return bool(groups)
