from lib.config.config_file import Config

config_obj = Config.get_config()

RULES_FILE_LOCATION = config_obj.get("RULES_FILE_LOCATION")

# rules field values

FROM = "from"
TO = "to"
CC = "cc"
BCC = "bcc"
REPLY = "reply"
RECEIVED_DATE = "received_date"
LABLES = "lables"
BODY = "body"
SUBJECT = "subject"

CONTAINS = "contains"
DOES_NOT_CONTAIN = "does not contain"
EQUALS = "equals"
DOES_NOT_EQUAL = "does not equal"
LESS_THAN = "less than"
GREATER_THAN = "greater than"

READ = "read"
UNREAD = "unread"
MOVE = "move"

ALL = "all"
ANY = "any"

DAY = "day"
MONTH = "month"


STRING_OPERATOR_TYPES = (CONTAINS, DOES_NOT_CONTAIN, EQUALS, DOES_NOT_EQUAL)
DATE_OPERATOR_TYPES = (LESS_THAN, GREATER_THAN)

STRING_FIELDS = (FROM, TO, CC, BCC, REPLY, LABLES, BODY, SUBJECT)
DATE_FIELDS = (RECEIVED_DATE, )

FIELDS_TYPES = STRING_FIELDS + DATE_FIELDS
OPERATOR_TYPES = STRING_OPERATOR_TYPES + DATE_OPERATOR_TYPES

COMBINATION_MAPPING = {
    STRING_FIELDS: STRING_OPERATOR_TYPES,
    DATE_FIELDS: DATE_OPERATOR_TYPES
}

ACTION_TYPES = (READ, UNREAD, MOVE)

CATEGORY_TYPES = (ALL, ANY)

CATEGORY_MAPPING = {
    ALL: " and ",
    ANY: " or "
}

OPERATOR_MAPPING = {
    CONTAINS: "rlike",
    DOES_NOT_CONTAIN: "not rlike",
    EQUALS: "=",
    DOES_NOT_EQUAL: "<>",
    LESS_THAN: "<",
    GREATER_THAN: ">"
}

FILED_MAPPING = {
    FROM: FROM + "_address",
    TO: TO + "_address",
    CC: CC + "_address",
    BCC: BCC + "_address",
    REPLY: REPLY + "_address",
    SUBJECT: "subject",
    RECEIVED_DATE: RECEIVED_DATE,
    LABLES: LABLES,
    BODY: BODY
}

DURATION_TYPE_TYPES = (DAY, MONTH)
VALIDATION = {
    "field": {"type": "string", "required": True, "enum": FIELDS_TYPES},
    "operator": {"type": "string", "required": True, "enum": OPERATOR_TYPES},
    "action_category": {"type": "string", "required": True, "enum": ACTION_TYPES},
    "rule_category": {"type": "string", "required": True, "enum": CATEGORY_TYPES},
    "duration_type": {"type": "string", "required": True, "enum": DURATION_TYPE_TYPES},
}

REVERSE_MAPPING = {
    READ: UNREAD,
    UNREAD: READ
}