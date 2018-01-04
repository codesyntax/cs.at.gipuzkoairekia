from Acquisition import aq_inner
from plone.app.contentlisting.interfaces import IContentListing
from Products.Five.browser import BrowserView


class TransparencyView(BrowserView):
    def sections(self):
        context = aq_inner(self.context)
        brains = context.getFolderContents({'portal_type': 'TransparencySection'})
        return IContentListing(brains)