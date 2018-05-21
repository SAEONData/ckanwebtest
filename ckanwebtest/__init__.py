import pkg_resources


def _static_content(filename):
    return pkg_resources.resource_string(__name__, 'static/' + filename).decode('utf-8')


CONFIG_FILE = pkg_resources.resource_filename(__name__, '../server.ini')

INDEX_HTML = _static_content('index.html')

ORGANIZATIONS_HTML = _static_content('organizations.html')
INFRASTRUCTURES_HTML = _static_content('infrastructures.html')
METADATA_COLLECTIONS_HTML = _static_content('metadata_collections.html')
METADATA_SCHEMAS_HTML = _static_content('metadata_schemas.html')
METADATA_MODELS_HTML = _static_content('metadata_models.html')
METADATA_RECORDS_HTML = _static_content('metadata_records.html')

WORKFLOW_STATES_HTML = _static_content('workflow_states.html')
WORKFLOW_TRANSITIONS_HTML = _static_content('workflow_transitions.html')
WORKFLOW_METRICS_HTML = _static_content('workflow_metrics.html')
WORKFLOW_RULES_HTML = _static_content('workflow_rules.html')

JSONAPI_METADATA_HTML = _static_content('jsonapi_metadata.html')
JSONAPI_INSTITUTIONS_HTML = _static_content('jsonapi_institutions.html')

SAMPLE_METADATA_JSON = _static_content('sample_metadata.json')
