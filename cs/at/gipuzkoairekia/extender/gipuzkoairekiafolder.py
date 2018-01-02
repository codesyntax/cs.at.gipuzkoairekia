from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from cs.at.gipuzkoairekia.interfaces import IGipuzkoaIrekiaFolder
from cs.at.gipuzkoairekia import _
from zope.component import adapts
from zope.component import adapter
from zope.interface import implements
from zope.interface import implementer
from Products.Archetypes.interfaces import IFieldDefaultProvider
from zope.globalrequest import getRequest

try:
    from Products.LinguaPlone import atapi
except ImportError:
    from Products.Archetypes import public as atapi


class MyStringField(ExtensionField, atapi.StringField):
    """A trivial field."""



@implementer(IFieldDefaultProvider)
@adapter(IGipuzkoaIrekiaFolder)
def default_language(context):
    request = getRequest()
    return request.get('LANGUAGE', 'eu')


class GipuzkoaIrekiaFolderExtender(object):
    adapts(IGipuzkoaIrekiaFolder)
    implements(ISchemaExtender)

    fields = [
        MyStringField(
            'institution_code',
            widget=atapi.StringWidget(
                label=_(u'Institution code (Open-data portal)'),
                description=_(u'Enter here the code of the institution'),
            )
        ),
        MyStringField(
            'group_id',
            widget=atapi.StringWidget(
                label=_(u'Institution code (Transpareceny portal)'),
                description=_(u'Enter here the code of the institution'),
            )
        ),
        MyStringField(
            'gipuzkoairekia_language',
            vocabulary=atapi.DisplayList([
                ('eu', _(u'Euskara')),
                ('es', _(u'Espanol')),
                ('en', _(u'English')),
            ]),
            widget=atapi.SelectionWidget(
                type='radio',
                label=_(u'Language'),
                description=_(u'Select the language in which the contents will be shown'),
            )
        ),



    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
