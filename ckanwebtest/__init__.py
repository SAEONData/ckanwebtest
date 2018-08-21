import pkg_resources

__version__ = pkg_resources.require('ckanwebtest')[0].version


def _static_content(filename):
    return pkg_resources.resource_string(__name__, 'static/' + filename).decode('utf-8')


CONFIG_FILE = pkg_resources.resource_filename(__name__, '../server.ini')

INDEX_HTML = _static_content('index.html')

ORGANIZATIONS_HTML = _static_content('organizations.html')
INFRASTRUCTURES_HTML = _static_content('infrastructures.html')
METADATA_COLLECTIONS_HTML = _static_content('metadata_collections.html')
METADATA_STANDARDS_HTML = _static_content('metadata_standards.html')
METADATA_MODELS_HTML = _static_content('metadata_models.html')
METADATA_RECORDS_HTML = _static_content('metadata_records.html')
METADATA_WORKFLOW_HTML = _static_content('metadata_workflow.html')

WORKFLOW_STATES_HTML = _static_content('workflow_states.html')
WORKFLOW_TRANSITIONS_HTML = _static_content('workflow_transitions.html')

VOCABULARIES_HTML = _static_content('vocabularies.html')

JSONAPI_METADATA_CREATE_HTML = _static_content('jsonapi_metadata_create.html')
JSONAPI_METADATA_LIST_HTML = _static_content('jsonapi_metadata_list.html')
JSONAPI_INSTITUTIONS_HTML = _static_content('jsonapi_institutions.html')

SAMPLE_METADATA_JSON = _static_content('sample_metadata.json')
