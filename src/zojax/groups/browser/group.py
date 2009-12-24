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
from zope.security import checkPermission
from zope.security.interfaces import Unauthorized
from zojax.layout.pagelet import BrowserPagelet
from zojax.content.space.browser.space import ContentSpace


class GroupView(ContentSpace, BrowserPagelet):

    def __call__(self, *args, **kw):
        if checkPermission('zojax.AccessGroup', self.context):
            return super(GroupView, self).__call__()

        return BrowserPagelet.__call__(self, *args, **kw)
