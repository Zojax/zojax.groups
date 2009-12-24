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
from zojax.blogger.interfaces import IBlog
from zojax.content.space.interfaces import ISpace


class GroupSearchPortlet(object):

    categories = ()

    def update(self):
        context = self.context
        while not ISpace.providedBy(context):
            context = context.__parent__

        try:
            blog = context.get('blog')
            if not IBlog.providedBy(blog):
                return
        except:
            return

        if 'category' not in blog:
            return

        categories = []
        for category in blog['category'].values():
            categories.append((category.title, category.__name__))

        categories.sort()
        self.categories = [{'name':name, 'title':title} for title, name in categories]

    def isAvailable(self):
        return bool(self.categories)
