from Acquisition import aq_inner
from Acquisition import aq_parent
from cs.at.gipuzkoairekia.interfaces import IGipuzkoaIrekiaFolder
from plone.memoize.ram import cache
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from xml.etree.ElementTree import fromstring
from xmljson import yahoo as bf
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import time
import requests


BASE_URL_SEARCH = 'http://api.gipuzkoairekia.eus/dataset/buscar?org={0}&numRes=9999'
BASE_URL_DATASET = 'http://api.gipuzkoairekia.eus/dataset/{0}'

CATEGORY_SEARCH_URL = 'http://api.gipuzkoairekia.eus//categoria/lista'

LANG_SUFFIX = {
    'es': '',
    'eu': 'Eu',
    'en': 'En'
}

TITLE_KEY = 'titulo'
DESCRIPTION_KEY = 'descripcion'
SOURCE_KEY = 'fuente'
NAME_KEY = 'nombre'



def _render_dataset_id(method, self, datasetid):
    return (datasetid, time.time() // 3600)

def _render_organization_id(method, self):
    return (self.get_organization_id(), time.time() // 3600)


@implementer(IPublishTraverse)
class OpenDataFolderView(BrowserView):

    temp = ViewPageTemplateFile('opendatafolder.pt')

    def publishTraverse(self, request, name):
        if not hasattr(self, 'subpath'):
            self.subpath = []

        self.subpath.append(name)
        return self

    def __call__(self):
        return self.temp(self.context)

    def is_subpath(self):
        return hasattr(self, 'subpath') and bool(self.subpath)


    def subpath_title(self):
        data = self.dataset_data()
        return data.get('title', '')

    def subpath_description(self):
        data = self.dataset_data()
        return data.get('description', '')

    def get_organization_id(self):
        context = aq_inner(self.context)
        while not (IGipuzkoaIrekiaFolder.providedBy(context) or IPloneSiteRoot.providedBy(context)):
            context = aq_parent(context)

        if IGipuzkoaIrekiaFolder.providedBy(context):
            return context.getField('institution_code').get(context)
        else:
            return None

    @cache(_render_organization_id)
    def category_data(self):
        try:
            data = requests.get(CATEGORY_SEARCH_URL, timeout=10)
            return bf.data(fromstring(data.content))
        except:
            return {'error': True}

    def get_category(self, id):
        language = self.get_language()
        categories = self.category_data()
        items = categories.get('resultado', {}).get('categorias', {}).get('categoria', [])
        new_data = {}
        for item in items:
            new_data[item.get('id')] = item.get(TITLE_KEY + LANG_SUFFIX.get(language))

        return new_data.get(id, '')


    @cache(_render_organization_id)
    def organization_data(self):
        organization = self.get_organization_id()
        url = BASE_URL_SEARCH.format(organization)
        try:
            data = requests.get(url, timeout=10)
            return bf.data(fromstring(data.content))
        except:
            return {'error': True}


    def dataset_data(self):
        language = self.get_language()
        data = self.one_dataset_data(self.subpath[0])
        if data.get('error', False):
            return {}
        else:
            item = data.get('resultado', {}).get('dataset', {})
            item['title'] = item.get(TITLE_KEY + LANG_SUFFIX.get(language))
            item['description'] = item.get(DESCRIPTION_KEY + LANG_SUFFIX.get(language))
            item['source'] = item.get(SOURCE_KEY + LANG_SUFFIX.get(language))

            new_resources = []

            for resource in item.get('recursos', {}).get('recurso', []):
                new_resource = resource
                new_resource['name'] = resource.get(NAME_KEY + LANG_SUFFIX.get(language))
                new_resource['description'] = resource.get(DESCRIPTION_KEY + LANG_SUFFIX.get(language))
                new_resources.append(new_resource)

            item['recursos']['recurso'] = new_resources
            return item



    @cache(_render_dataset_id)
    def one_dataset_data(self, dataset):
        url = BASE_URL_DATASET.format(dataset)
        try:
            data = requests.get(url, timeout=10)
            return bf.data(fromstring(data.content))
        except:
            return {'error': True}


    def datasets(self):
        data = self.organization_data()
        datasets = data.get('resultado', {}).get('datasets', {}).get('dataset', [])
        for dataset in datasets:
            yield self.decorate_dataset(dataset)

    def get_language(self):
        return self.context.Language()

    def decorate_dataset(self, item):
        language = self.get_language()
        item['title'] = item.get(TITLE_KEY + LANG_SUFFIX.get(language))
        item['description'] = item.get(DESCRIPTION_KEY + LANG_SUFFIX.get(language))
        item['source'] = item.get(SOURCE_KEY + LANG_SUFFIX.get(language))
        return item
