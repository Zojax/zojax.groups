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
from zope import interface, component
from zope.component import getUtility
from zope.security import checkPermission
from zope.traversing.browser import absoluteURL
from zope.publisher.interfaces import NotFound
from zope.app.intid.interfaces import IIntIds
from zope.app.security.interfaces import IUnauthenticatedPrincipal

from zojax.layoutform import button, Fields, PageletForm, interfaces
from zojax.catalog.interfaces import ICatalog
from zojax.content.actions.action import Action
from zojax.preferences.interfaces import IRootPreferences
from zojax.principal.invite.interfaces import IInvitations
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.members.interfaces import IMembers, IMembersAware

from interfaces import _, IInviteMemberForm, IInviteMemberAction


class InviteMemberAction(Action):
    interface.implements(IInviteMemberAction)
    component.adapts(IRootPreferences, interface.Interface)

    title = _('Invite to my groups')
    weight = 99998

    @property
    def url(self):
        return '%s/groupinvite.html'%absoluteURL(self.context, self.request)

    def isAvailable(self):
        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            return False

        principal = self.context.__principal__
        principalId = principal.id

        if self.request.principal.id == principalId:
            return False

        invitations = [
            invitation.object.id for invitation in
            getUtility(IInvitations).getInvitationsByPrincipal(
                principalId, ('invitation.member',))]

        for group in getUtility(ICatalog).searchResults(
            type = {'any_of': ('content.group',)},
            members = {'any_of': (self.request.principal.id,)}):

            if group.id in invitations:
                continue

            if principalId not in group.members and \
                    checkPermission('zojax.InviteGroupMember', group):
                return True

        return False


class InviteMemberForm(PageletForm):

    fields = Fields(IInviteMemberForm)

    @property
    def label(self):
        return _(u'Invite ${user} to my groups',
                 mapping={'user': self.context.__principal__.title})

    def getContent(self):
        principal = IPersonalProfile(self.context.__principal__).title
        mytitle = IPersonalProfile(self.request.principal).title
        return {'message': u'Hello %s,\n\nJoin to my groups!\n\nRegards,\n%s'%(
                principal, mytitle)}

    @button.buttonAndHandler(_(u'Invite'), provides=interfaces.IAddButton)
    def handleSend(self, action):
        request = self.request
        data, errors = self.extractData()

        if errors:
            IStatusMessage(request).add(self.formErrorsMessage, 'error')
        else:
            ids = getUtility(IIntIds)

            message = data['message']
            principal = self.context.__principal__.id

            for gid in data['groups']:
                group = ids.queryObject(gid)
                if group is not None:
                    group.members.invite(principal, message)

            IStatusMessage(request).add(_(u'Invitation has been sent.'))
            self.redirect('.')

    @button.buttonAndHandler(_(u'Cancel'), provides=interfaces.ICancelButton)
    def handleCancel(self, action):
        self.redirect('.')

    def render(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            return super(InviteMemberForm, self).render()

        raise NotFound(self, self.__name__, self.request)
