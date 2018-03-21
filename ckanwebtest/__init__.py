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
JSONAPI_METADATA_HTML = _static_content('jsonapi_metadata.html')
SAMPLE_METADATA_JSON = _static_content('sample_metadata.json')
