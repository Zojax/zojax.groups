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
from zope.dublincore.interfaces import IDCTimes
from zope.index.text.parsetree import ParseError

from zojax.groups.types import types
from zojax.batching.batch import Batch
from zojax.catalog.interfaces import ICatalog
from zojax.filefield.interfaces import IImage
from zojax.ownership.interfaces import IOwnership
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.groups.interfaces import _


class BrowseGroups(object):

    batch = Batch((), 15)

    def update(self):
        context = self.context
        request = self.request

        self.hasGroups = bool(len(context))
        if not self.hasGroups:
            return

        if 'form.search.clear' in request:
            self.redirect('./index.html')
            return

        catalog = getUtility(ICatalog)

        if 'form.search' in request:
            s = request.get('form.searchText', u'').strip()
            if s:
                query = {
                    'type': {'any_of': ('content.group',)},
                    'searchContext': (context,),
                    'searchableText': s}

                try:
                    results = catalog.searchResults(**query)
                except ParseError, e:
                    IStatusMessage(request).add(e, 'error')
                    return

                self.batch = Batch(
                    results, size=15, context=context, request=request)
            else:
                IStatusMessage(request).add(
                    _('Please enter one or more words for search.'), 'warning')
            return

        results = catalog.searchResults(
            type = {'any_of': ('content.group',)},
            searchContext = (context,), sort_on='title')

        if not results:
            self.hasGroups = False
            return

        self.batch = Batch(results, size=15, context=context, request=request)

    def getGroupInfo(self, group):
        dc = IDCTimes(group)
        principal = getattr(IOwnership(group, None), 'owner', None)

        info = {
            'id': id,
            'title': group.title,
            'description': group.description,
            'owner': principal,
            'created': dc.created,
            'members': len(group['members']),
            'default': not bool(group.logo),
            'gtype': types.getTerm(group.gtype)}
        return info
