# -*- coding: utf-8 -*-
"""Base module for unittesting."""
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.testing import z2
import unittest2 as unittest

import ploneintranet.userprofile
import ploneintranet.microblog
import ploneintranet.microblog.statuscontainer


class PloneintranetApiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=ploneintranet.userprofile)
        self.loadZCML(package=ploneintranet.microblog)
        # Force status updates to be immediately written
        ploneintranet.microblog.statuscontainer.MAX_QUEUE_AGE = 0
        z2.installProduct(app, 'Products.membrane')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ploneintranet.userprofile:default')
        applyProfile(portal, 'ploneintranet.microblog:default')

    def tearDownZope(self, app):
        # Reset status update queue age
        ploneintranet.microblog.statuscontainer.MAX_QUEUE_AGE = 1000
        z2.uninstallProduct(app, 'Products.membrane')


FIXTURE = PloneintranetApiLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="PloneintranetApiLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="PloneintranetApiLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.portal.REQUEST

    def login(self, username):
        login(self.portal, username)


class FunctionalTestCase(IntegrationTestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
