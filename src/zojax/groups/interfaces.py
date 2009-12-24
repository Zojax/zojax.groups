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
""" Groups interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory

from zojax.richtext.field import RichText
from zojax.filefield.field import ImageField
from zojax.widget.radio.field import RadioChoice
from zojax.widget.checkbox.field import CheckboxList
from zojax.content.type.interfaces import IItem
from zojax.content.space.interfaces import ISpace, IWorkspace, IWorkspaceFactory
from zojax.content.activity.interfaces import IContentActivityRecord
from zojax.principal.invite.interfaces import IObjectInvitation
from zojax.groups import types, vocabulary

from zojax.members.interfaces import IMember as IGroupMember
from zojax.members.interfaces import IMembers as IGroupMembers

_ = MessageFactory('zojax.groups')


class IGroup(IItem, ISpace):
    """ iternal team info """

    members = interface.Attribute('IGroupMembers object')

    gtype = RadioChoice(
        title = _(u'Group type'),
        description = _(u'Select type for this group.'),
        vocabulary = types.types,
        default = 'open',
        required = False)

    logo = ImageField(
        title = _('Logo'),
        description = _('Group logo'),
        maxWidth = 250, maxHeight = 190, scale = True,
        required = False)

    text = RichText(
        title = _(u'Text'),
        description = _(u'Group long description.'),
        required = False)


class IGroups(IItem, IWorkspace):
    """ team folder """


class IGroupsWorkspaceFactory(IWorkspaceFactory):
    """ groups woprkspace factory """
