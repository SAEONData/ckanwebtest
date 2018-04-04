#!/usr/bin/env python
import cherrypy
import re

from ckanwebtest import *
from ckanapi import RemoteCKAN


@cherrypy.popargs('action_name')
class Action:

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def index(self, action_name):
        data = cherrypy.request.json
        url = cherrypy.config['ckan.url']
        apikey = cherrypy.config['ckan.apikey']
        get_only = action_name.endswith(('_list', '_show'))

        with RemoteCKAN(url, apikey=apikey, get_only=get_only) as ckan:
            try:
                return ckan.call_action(action_name, data_dict=data)

            except Exception as e:
                # return a structured error message if available
                if len(e.args) > 0 and type(e.args[0]) is not str:
                    return e.args[0]
                else:
                    # otherwise return the exception string; if an HTML error doc was returned
                    # from CKAN, strip it out and replace with debug url if possible
                    debug_match = re.search(r'\bdebug_count = ([0-9]+)\b', str(e))
                    if debug_match:
                        info = "'{}/_debug/view/{}'".format(url, debug_match.group(1))
                    else:
                        info = "'Server Error'"
                    return re.sub(r"'<!DOCTYPE html .*</html>.*'", info, str(e))


class Application:

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
    def jsonapi_institutions(self):
        jsonapi_url = cherrypy.config['jsonapi.url']
        return JSONAPI_INSTITUTIONS_HTML \
            .replace('JSONAPI_URL', jsonapi_url)

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

    @cherrypy.expose
    def metadata_records(self):
        return METADATA_RECORDS_HTML \
            .replace('SAMPLE_METADATA_JSON', SAMPLE_METADATA_JSON)


if __name__ == "__main__":
    cherrypy.config.update(CONFIG_FILE)
    cherrypy.tree.mount(Application(), '/')
    cherrypy.tree.mount(Action(), '/action', config={'/': {'tools.trailing_slash.on': False}})
    cherrypy.engine.start()
    cherrypy.engine.block()
