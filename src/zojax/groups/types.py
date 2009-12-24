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
from zope import component
from zope.i18nmessageid import MessageFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

_ = MessageFactory('zojax.groups')


tp1 = SimpleTerm('open', 'open', _('Open Group'))
tp1.description = _('Non-members can view content and participate.')

tp2 = SimpleTerm('members', 'members', _('Members Only Group'))
tp2.description = _('Non-members can view content, but must join to participate.')

tp3 = SimpleTerm('private', 'private', _('Private Group'))
tp3.description = _('Only members can view content and participate.')

tp4 = SimpleTerm('secret', 'secret', _('Secret Group'))
tp4.description = _('Only members may participate, and the group '
                    'is not listed in the group directory.')

types = SimpleVocabulary((tp1, tp2, tp3, tp4))
