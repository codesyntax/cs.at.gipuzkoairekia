"""Definition of the TransparencySection content type
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
from cs.at.gipuzkoairekia.interfaces import ITransparencySection
from cs.at.gipuzkoairekia.config import PROJECTNAME

TransparencySectionSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    ImageField(
        'image',
        required=False,
        sizes={
            'large'   : (768, 768),
            'preview' : (400, 400),
            'mini'    : (200, 200),
            'thumb'   : (128, 128),
            'tile'    :  (64, 64),
            'icon'    :  (32, 32),
            'listing' :  (16, 16),
        },
        widget=ImageWidget(
            label=_(u'Logo'),
            show_content_type=False,
        ),
    ),

    atapi.StringField(
        'category_id',
        languageIndependent=True,
        required=True,
        widget=atapi.StringWidget(
            label=_(u'Category id'),
            description=_(u'Enter the transparency portal category id to be linked here'),
        )
    )

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

TransparencySectionSchema['title'].storage = atapi.AnnotationStorage()
TransparencySectionSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(TransparencySectionSchema, moveDiscussion=False)


class TransparencySection(base.ATCTContent):
    """Content-type for sections"""
    implements(ITransparencySection)

    meta_type = "TransparencySection"
    schema = TransparencySectionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    def image_url(self):
        return str(self.restrictedTraverse('@@images').scale('image', scale='mini'))

atapi.registerType(TransparencySection, PROJECTNAME)
