#!/usr/bin/env python
import cherrypy
import re
from requests_oauthlib import OAuth2Session
from urllib.parse import urljoin
from oauthlib.oauth2 import OAuth2Error
from ckanapi import RemoteCKAN

from ckanwebtest import __version__
from ckanwebtest import *

_ckan_apikey = None


def authorize(func):
    """
    Decorator which authorizes this application if not already authorized, before
    executing the decorated function.
    """
    def wrapper(*args, **kwargs):
        if not _ckan_apikey and not logged_in():
            raise cherrypy.HTTPRedirect('/auth/login')
        return func(*args, **kwargs)

    return wrapper


def authorized(func):
    """
    Decorator which only allows the function to be executed if this application
    is already authorized.
    """
    def wrapper(*args, **kwargs):
        if not _ckan_apikey and not logged_in():
            raise cherrypy.HTTPError(403)
        return func(*args, **kwargs)

    return wrapper


def logged_in():
    return cherrypy.session.get('oauth2_token')


def login_error():
    return cherrypy.session.get('oauth2_error')


class Auth:

    def __init__(self):
        self.authorization_url = cherrypy.config['auth.authorization_url']
        self.token_url = cherrypy.config['auth.token_url']
        self.client_id = cherrypy.config['auth.client_id']
        self.client_secret = cherrypy.config['auth.client_secret']
        self.scopes = cherrypy.config['auth.scopes']

    @cherrypy.expose
    def login(self):
        oauth2session = OAuth2Session(client_id=self.client_id,
                                      scope=self.scopes,
                                      redirect_uri=urljoin(cherrypy.url(), 'callback'))
        authorization_url, state = oauth2session.authorization_url(self.authorization_url)
        cherrypy.session['oauth2_state'] = state
        raise cherrypy.HTTPRedirect(authorization_url)

    @cherrypy.expose
    def callback(self, **kwargs):
        oauth2session = OAuth2Session(client_id=self.client_id,
                                      state=cherrypy.session['oauth2_state'],
                                      redirect_uri=urljoin(cherrypy.url(), 'callback'))
        try:
            token = oauth2session.fetch_token(self.token_url,
                                              client_secret=self.client_secret,
                                              authorization_response=cherrypy.url(qs=cherrypy.request.query_string))
            cherrypy.session['oauth2_token'] = token
            cherrypy.session['oauth2_error'] = None
        except OAuth2Error as e:
            cherrypy.session['oauth2_token'] = None
            cherrypy.session['oauth2_error'] = str(e)

        raise cherrypy.HTTPRedirect('/')


@cherrypy.popargs('action_name')
class Action:

    def __init__(self):
        self.ckan_url = cherrypy.config['ckan.url']
        self.client_id = cherrypy.config['auth.client_id']

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    @authorized
    def index(self, action_name):
        session = OAuth2Session(client_id=self.client_id, token=cherrypy.session['oauth2_token']) if not _ckan_apikey else None
        data = cherrypy.request.json
        get_only = action_name.endswith(('_list', '_show'))

        with RemoteCKAN(self.ckan_url, session=session, get_only=get_only, apikey=_ckan_apikey) as ckan:
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
                        info = "'{}/_debug/view/{}'".format(self.ckan_url, debug_match.group(1))
                    else:
                        info = "'Server Error'"
                    return re.sub(r"'<!DOCTYPE html .*</html>.*'", info, str(e))


class Application:

    def __init__(self):
        self.jsonapi_url = cherrypy.config['jsonapi.url']

    @cherrypy.expose
    def index(self):
        if _ckan_apikey:
            login_msg = 'Using CKAN API key.'
            login_hidden = 'hidden'
        elif logged_in():
            login_msg = 'You are logged in.'
            login_hidden = 'hidden'
        elif login_error():
            login_msg = 'Login failed. ' + login_error()
            login_hidden = ''
        else:
            login_msg = 'You are not logged in.'
            login_hidden = ''

        return INDEX_HTML \
            .replace('VERSION', __version__) \
            .replace('LOGIN_MESSAGE', login_msg) \
            .replace('LOGIN_HIDDEN', login_hidden)

    @cherrypy.expose
    @authorize
    def jsonapi_metadata_create(self):
        return JSONAPI_METADATA_CREATE_HTML \
            .replace('JSONAPI_URL', self.jsonapi_url) \
            .replace('SAMPLE_METADATA_JSON', SAMPLE_METADATA_JSON)

    @cherrypy.expose
    @authorize
    def jsonapi_metadata_list(self):
        return JSONAPI_METADATA_LIST_HTML \
            .replace('JSONAPI_URL', self.jsonapi_url)

    @cherrypy.expose
    @authorize
    def jsonapi_institutions(self):
        return JSONAPI_INSTITUTIONS_HTML \
            .replace('JSONAPI_URL', self.jsonapi_url)

    @cherrypy.expose
    @authorize
    def organizations(self):
        return ORGANIZATIONS_HTML

    @cherrypy.expose
    @authorize
    def infrastructures(self):
        return INFRASTRUCTURES_HTML

    @cherrypy.expose
    @authorize
    def metadata_collections(self):
        return METADATA_COLLECTIONS_HTML

    @cherrypy.expose
    @authorize
    def metadata_schemas(self):
        return METADATA_SCHEMAS_HTML

    @cherrypy.expose
    @authorize
    def metadata_models(self):
        return METADATA_MODELS_HTML

    @cherrypy.expose
    @authorize
    def metadata_records(self):
        return METADATA_RECORDS_HTML \
            .replace('SAMPLE_METADATA_JSON', SAMPLE_METADATA_JSON)

    @cherrypy.expose
    @authorize
    def workflow_states(self):
        return WORKFLOW_STATES_HTML

    @cherrypy.expose
    @authorize
    def workflow_transitions(self):
        return WORKFLOW_TRANSITIONS_HTML

    @cherrypy.expose
    @authorize
    def workflow_metrics(self):
        return WORKFLOW_METRICS_HTML

    @cherrypy.expose
    @authorize
    def workflow_rules(self):
        return WORKFLOW_RULES_HTML

    @cherrypy.expose
    @authorize
    def vocabularies(self):
        return VOCABULARIES_HTML


if __name__ == "__main__":
    cherrypy.config.update(CONFIG_FILE)
    if cherrypy.config.get('auth.insecure_transport'):
        import os
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    _ckan_apikey = cherrypy.config.get('ckan.apikey')

    cherrypy.tree.mount(Application(), '/', config={'/': {'tools.sessions.on': True}})

    cherrypy.tree.mount(Action(), '/action', config={'/': {'tools.sessions.on': True,
                                                           'tools.trailing_slash.on': False}})

    cherrypy.tree.mount(Auth(), '/auth', config={'/': {'tools.sessions.on': True,
                                                       'tools.trailing_slash.on': False}})

    cherrypy.engine.start()
    cherrypy.engine.block()
