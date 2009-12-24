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
from zope import schema, interface
from zojax.portlet.interfaces import _ as pMsg
from zojax.portlet.interfaces import statusVocabulary, ENABLED, DISABLED
from zojax.portlet.interfaces import \
    IPortletManagerWithStatus, ENABLED, statusVocabulary
from zojax.groups.interfaces import _


class IGroupsRightPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.yourgroups', 'portlet.actions', 'portlet.activity',),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class IGroupsLeftPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = (),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class IGroupLeftPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = (),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class IGroupRightPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.actions',
                   'portlet.recentlyjoined',
                   'portlet.comments',),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class IGroupContentPortletManager(IPortletManagerWithStatus):

    portletIds = schema.Tuple(
        title = pMsg('Portlets'),
        value_type = schema.Choice(vocabulary = 'zojax portlets'),
        default = ('portlet.groupoverview',),
        required = True)

    status = schema.Choice(
        title = pMsg(u'Status'),
        vocabulary = statusVocabulary,
        default = ENABLED,
        required = True)


class IGroupSearchPortlet(interface.Interface):
    """ group search portlet """


class IGroupOverviewPortlet(interface.Interface):
    """ group overview portlet """


class IGroupOverviewContentPortlet(interface.Interface):
    """ group overview portlet """

    showLogo = schema.Bool(
        title = _('Show group logo'),
        default = True,
        required = True)


class IYourGroupsPortlet(interface.Interface):
    """ your groups portlet """
