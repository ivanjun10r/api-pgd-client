from .. import namedtuples

AUTHORIZATION_HEADER_LABEL = "Authorization"
AUTHORIZATION_HEADER = namedtuples.HeaderItem(
    AUTHORIZATION_HEADER_LABEL, "{token_type} {access_token}"
)
CONTENT_TYPE_HEADER_LABEL = "Content-Type"
CONTENT_TYPE_JSON_VALUE = "application/json"
CONTENT_TYPE_JSON_HEADER = namedtuples.HeaderItem(
    CONTENT_TYPE_HEADER_LABEL, CONTENT_TYPE_JSON_VALUE
)
CONTENT_TYPE_X_FORM_VALUE = "application/x-www-form-urlencoded"
CONTENT_TYPE_FORM_URLENCODED_HEADER = namedtuples.HeaderItem(
    CONTENT_TYPE_HEADER_LABEL, CONTENT_TYPE_X_FORM_VALUE
)
USER_AGENT_HEADER_LABEL = "User-Agent"
USER_AGENT_HEADER = namedtuples.HeaderItem(
    USER_AGENT_HEADER_LABEL, "{system_name}/{system_version} ({system_url})"
)
