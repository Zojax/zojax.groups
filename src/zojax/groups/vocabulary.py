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
from zope import interface
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.security import checkPermission
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

import zojax.groups.interfaces
from zojax.catalog.utils import getRequest
from zojax.catalog.interfaces import ICatalog

_ = MessageFactory('zojax.groups')


class YourGroupsVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        request = getRequest()
        if request is None:
            return SimpleVocabulary(())

        results = getUtility(ICatalog).searchResults(
            type = {'any_of': ('content.group',)},
            members = {'any_of': (request.principal.id,)})

        groups = []
        for group in results:
            term = SimpleTerm(group.id, str(group.id), group.title)
            term.description = group.description

            groups.append((group.title, term))

        groups.sort()
        return SimpleVocabulary([term for _t, term in groups])


class YourInvitableGroupsVocabulary(object):
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        request = getRequest()
        if request is None:
            return SimpleVocabulary(())

        results = getUtility(ICatalog).searchResults(
            type = {'any_of': ('content.group',)},
            members = {'any_of': (request.principal.id,)})

        groups = []
        for group in results:
            if checkPermission('zojax.InviteGroupMember', group):
                term = SimpleTerm(group.id, str(group.id), group.title)
                term.description = group.description

                groups.append((group.title, term))

        groups.sort()
        return SimpleVocabulary([term for _t, term in groups])
