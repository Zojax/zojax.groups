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
from zope import interface, component, event
from zope.lifecycleevent import ObjectCreatedEvent
from zope.security.proxy import removeSecurityProxy
from zojax.content.space.interfaces import IRootSpace
from zojax.content.space.workspace import WorkspaceFactory
from zojax.content.type.container import ContentContainer

from interfaces import _, IGroups, IGroupsWorkspaceFactory


class GroupsWorkspace(ContentContainer):
    interface.implements(IGroups)


class GroupsWorkspaceFactory(WorkspaceFactory):
    component.adapts(IRootSpace)
    interface.implements(IGroupsWorkspaceFactory)

    name = 'groups'
    weight = 99999
    description = _(u'Personal spaces for groups.')
    factory = GroupsWorkspace

    @property
    def title(self):
        if self.isInstalled():
            return self.space['groups'].title
        else:
            return _(u'Groups')
