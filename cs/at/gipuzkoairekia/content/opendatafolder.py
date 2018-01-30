# -*- coding: utf-8 -*-
"""Definition of the OpenDataFolder content type
"""

from zope.interface import implements

try:
    from Products.LinguaPlone import atapi
except ImportError:
    from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from plone.app.blob.field import ImageField, ImageWidget
# -*- Message Factory Imported Here -*-
from cs.at.gipuzkoairekia import _
from cs.at.gipuzkoairekia.interfaces import IOpenDataFolder
from cs.at.gipuzkoairekia.config import PROJECTNAME

OpenDataFolderSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

OpenDataFolderSchema['title'].storage = atapi.AnnotationStorage()
OpenDataFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(OpenDataFolderSchema, moveDiscussion=False)


class OpenDataFolder(base.ATCTContent):
    """Content-type for sections"""
    implements(IOpenDataFolder)

    meta_type = "OpenDataFolder"
    schema = OpenDataFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(OpenDataFolder, PROJECTNAME)
