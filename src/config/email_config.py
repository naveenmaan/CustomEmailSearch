from lib.config.config_file import Config

config_obj = Config.get_config()

USER_AUTH_STORAGE_PATH = config_obj.get("USER_AUTH_STORAGE_PATH")
CREDENTIAL_STORAGE_PATH = config_obj.get("CREDENTIAL_STORAGE_PATH")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

GMAIL = "gmail"
VERSION_1 = "v1"

MAX_EMAIL_COUNT = 10
UNREAD_QUERY = "is:unread"

GMAIL_HEADER_MAPPER = {
    "Subject": "subject",
    "From": "from_address",
    "To": "to_addresses",
    "Cc": "cc_addresses",
    "Bcc": "bcc_addresses",
    "Reply-To": "reply_address",
    "Date": "received_date"
}

CREATED_BY = "EMAIL_PROCESSING_MANAGER"
