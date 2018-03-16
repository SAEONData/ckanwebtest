#!/usr/bin/env python
import cherrypy
import json

from ckanwebtest import *
from ckanapi import RemoteCKAN


class Action:

    @cherrypy.expose
    def index(self, action_name, **kwargs):
        url = cherrypy.config['ckan.url']
        apikey = cherrypy.config['ckan.apikey']
        get_only = action_name.endswith('_list')

        with RemoteCKAN(url, apikey=apikey, get_only=get_only) as ckan:
            try:
                result = ckan.call_action(action_name, data_dict=kwargs)
            except Exception as e:
                result = e.args[0] if len(e.args) == 1 else e.args

        return json.dumps(result, indent=4)


class Application:

    def __init__(self):
        self._action = Action()

    def _cp_dispatch(self, vpath):
        if len(vpath) > 1 and vpath[0] == 'action':
            vpath.pop(0)
            cherrypy.request.params['action_name'] = vpath.pop(0)
            return self._action
        return vpath

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
    def infrastructures(self):
        return INFRASTRUCTURES_HTML

    @cherrypy.expose
    def metadata_collections(self):
        return METADATA_COLLECTIONS_HTML

    @cherrypy.expose
    def metadata_schemas(self):
        return METADATA_SCHEMAS_HTML

    @cherrypy.expose
    def metadata_models(self):
        return METADATA_MODELS_HTML


if __name__ == "__main__":
    cherrypy.config.update(CONFIG_FILE)
    cherrypy.quickstart(Application())
