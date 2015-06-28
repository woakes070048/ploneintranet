from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import (
    PersonalBarViewlet as BasePersonalBarViewlet
)
from ploneintranet import api as pi_api


class PersonalBarViewlet(BasePersonalBarViewlet):

    index = ViewPageTemplateFile('personal_bar.pt')

    def update(self):
        super(PersonalBarViewlet, self).update()
        member = self.portal_state.member()
        userid = member.getId()
        self.avatar_url = pi_api.userprofile.avatar_url(userid)
