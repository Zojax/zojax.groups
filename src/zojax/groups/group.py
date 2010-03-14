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
from zope.component import getUtility, queryMultiAdapter
from zope.security.proxy import removeSecurityProxy
from zope.app.intid.interfaces import IIntIds
from zope.copypastemove.interfaces import IObjectCopier
from zope.lifecycleevent import ObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.richtext.field import RichTextProperty
from zojax.filefield.field import FileFieldProperty
from zojax.content.type.container import ContentContainer
from zojax.content.type.searchable import ContentSearchableText
from zojax.content.space.interfaces import IWorkspacesManagement
from zojax.content.permissions.utils import updatePermissions
from zojax.permissionsmap.interfaces import IObjectPermissionsMapsManager
from zojax.members.interfaces import IMembersAware
from zojax.members.members import Members

from interfaces import IGroup


class Group(ContentContainer):
    interface.implements(IGroup, IMembersAware, IWorkspacesManagement)

    showTabs = True
    showHeader = True
    workspaces = ('overview',)
    enabledWorkspaces = ()
    defaultWorkspace = 'overview'
    gtype = 'open'

    logo = FileFieldProperty(IGroup['logo'])
    text = RichTextProperty(IGroup['text'])

    @property
    def id(self):
        return getUtility(IIntIds).getId(self)

    @property
    def members(self):
        if 'members' not in self:
            members = Members()
            event.notify(ObjectCreatedEvent(members))
            self['members'] = members
        return self['members']

    def isEnabled(self, workspaceFactory):
        if workspaceFactory.name == 'members':
            return True

        return workspaceFactory.isAvailable() and \
            workspaceFactory.name in self.workspaces


@component.adapter(IGroup, IObjectModifiedEvent)
def groupModified(group, ev):
    if not group.gtype:
        group.gtype = u'open'

    IObjectPermissionsMapsManager(
        removeSecurityProxy(group)).set(('group.%s'%group.gtype,))

    updatePermissions(group)


class GroupSearchableText(ContentSearchableText):
    component.adapts(IGroup)

    def getSearchableText(self):
        text = super(GroupSearchableText, self).getSearchableText()

        try:
            return text + u' ' + self.content.text.text
        except AttributeError:
            return text


class GroupCopier(object):
    component.adapts(IGroup)
    interface.implements(IObjectCopier)

    def __init__(self, object):
        self.context = object

    def copyTo(self, target, new_name=None):
        raise RuntimeError('Object is not copyable')

    def copyable(self):
        return False

    def copyableTo(self, target, name=None):
        return False
