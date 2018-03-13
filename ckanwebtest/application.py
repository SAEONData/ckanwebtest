#!/usr/bin/env python
import cherrypy
import json

from ckanwebtest import *
from ckanapi import RemoteCKAN


class Application:

    @staticmethod
    def _call_ckan(action, **kwargs):
        url = cherrypy.config['ckan.url']
        apikey = cherrypy.config['ckan.apikey']
        get_only = action.endswith('_list')

        with RemoteCKAN(url, apikey=apikey, get_only=get_only) as ckan:
            try:
                result = ckan.call_action(action, data_dict=kwargs)
            except Exception as e:
                result = e.args[0] if len(e.args) == 1 else e.args

        return json.dumps(result, indent=4)

    @cherrypy.expose
    def index(self):
        return INDEX_HTML

    @cherrypy.expose
    def jsonapi_metadata(self):
        jsonapi_url = cherrypy.config['jsonapi.url']
        return JSONAPI_METADATA_HTML \
            .replace('JSONAPI_URL', jsonapi_url) \
            .replace('SAMPLE_METADATA_JSON', SAMPLE_METADATA_JSON)

    @cherrypy.expose
    def organizations(self):
        return ORGANIZATIONS_HTML

    @cherrypy.expose
    def organization_list(self):
        return self._call_ckan('organization_list', all_fields=True)

    @cherrypy.expose
    def organization_create(self, **kwargs):
        return self._call_ckan('organization_create', **kwargs)

    @cherrypy.expose
    def organization_update(self, **kwargs):
        return self._call_ckan('organization_update', **kwargs)

    @cherrypy.expose
    def organization_delete(self, **kwargs):
        return self._call_ckan('organization_delete', **kwargs)

    @cherrypy.expose
    def infrastructures(self):
        return INFRASTRUCTURES_HTML

    @cherrypy.expose
    def infrastructure_list(self):
        return self._call_ckan('infrastructure_list', all_fields=True)

    @cherrypy.expose
    def infrastructure_create(self, **kwargs):
        return self._call_ckan('infrastructure_create', **kwargs)

    @cherrypy.expose
    def infrastructure_update(self, **kwargs):
        return self._call_ckan('infrastructure_update', **kwargs)

    @cherrypy.expose
    def infrastructure_delete(self, **kwargs):
        return self._call_ckan('infrastructure_delete', **kwargs)

    @cherrypy.expose
    def metadata_collections(self):
        return METADATA_COLLECTIONS_HTML

    @cherrypy.expose
    def metadata_collection_list(self):
        return self._call_ckan('metadata_collection_list', all_fields=True)

    @cherrypy.expose
    def metadata_collection_create(self, **kwargs):
        return self._call_ckan('metadata_collection_create', **kwargs)

    @cherrypy.expose
    def metadata_collection_update(self, **kwargs):
        return self._call_ckan('metadata_collection_update', **kwargs)

    @cherrypy.expose
    def metadata_collection_delete(self, **kwargs):
        return self._call_ckan('metadata_collection_delete', **kwargs)

    @cherrypy.expose
    def metadata_schemas(self):
        return METADATA_SCHEMAS_HTML

    @cherrypy.expose
    def metadata_schema_list(self):
        return self._call_ckan('metadata_schema_list')

    @cherrypy.expose
    def metadata_schema_create(self, **kwargs):
        return self._call_ckan('metadata_schema_create', **kwargs)

    @cherrypy.expose
    def metadata_schema_update(self, **kwargs):
        return self._call_ckan('metadata_schema_update', **kwargs)

    @cherrypy.expose
    def metadata_schema_delete(self, **kwargs):
        return self._call_ckan('metadata_schema_delete', **kwargs)

    @cherrypy.expose
    def metadata_models(self):
        return METADATA_MODELS_HTML

    @cherrypy.expose
    def metadata_model_list(self):
        return self._call_ckan('metadata_model_list')

    @cherrypy.expose
    def metadata_model_create(self, **kwargs):
        return self._call_ckan('metadata_model_create', **kwargs)

    @cherrypy.expose
    def metadata_model_update(self, **kwargs):
        return self._call_ckan('metadata_model_update', **kwargs)

    @cherrypy.expose
    def metadata_model_delete(self, **kwargs):
        return self._call_ckan('metadata_model_delete', **kwargs)


if __name__ == "__main__":
    cherrypy.config.update(CONFIG_FILE)
    cherrypy.quickstart(Application())
