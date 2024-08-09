import os.path
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from src.config.email_config import USER_AUTH_STORAGE_PATH, SCOPES, CREDENTIAL_STORAGE_PATH, GMAIL, VERSION_1, \
    MAX_EMAIL_COUNT, UNREAD_QUERY


class GMailManager:

    def __init__(self):
        """
        method to init the required resources
        """

        self.credentials_obj = None
        self.get_user_authentication_credential()
        self.service = build(GMAIL, VERSION_1, credentials=self.credentials_obj)

    def get_user_authentication_credential(self):
        """
        method to get the user authentication credentials
        :return:
        """

        if os.path.exists(USER_AUTH_STORAGE_PATH):
            with open(USER_AUTH_STORAGE_PATH, 'rb') as token:
                self.credentials_obj = pickle.load(token)

        if not self.credentials_obj:
            self.authenticate_user()
            self.store_credential()
        elif not self.credentials_obj.valid:
            self.refresh_authentication_credential()
            self.store_credential()

    def refresh_authentication_credential(self):
        """
        method to refresh the customer credential
        :return:
        """

        if not self.credentials_obj or not self.credentials_obj.expired:
            return

        self.credentials_obj.refresh(Request())

    def authenticate_user(self):
        """
        method to authenticate the customer and store the credential to the system
        :return:
        """

        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_STORAGE_PATH, SCOPES)
        self.credentials_obj = flow.run_local_server(port=0)

    def store_credential(self):
        """
        method to store the authentication credential
        :return:
        """

        with open(USER_AUTH_STORAGE_PATH, 'wb') as token:
            pickle.dump(self.credentials_obj, token)

    def get_email_detail(self, message_id):
        """
        method to get the email details from the message_id
        :param message_id: 123456
        :return: dict({})
        """

        email_details = self.service.users().messages().get(userId='me', id=message_id).execute()
        return email_details

    def get_unread_email(self):
        """
        method to get the list of emails
        :return:
        """

        result = self.service.users().messages().list(maxResults=MAX_EMAIL_COUNT,
                                                      userId='me',
                                                      q=UNREAD_QUERY).execute()

        messages = result.get('messages')

        return messages

    def get_user_label_list(self):
        """
        method to get the user label list in system
        :return:
        """

        labels_list = self.service.users().labels().list(userId='me').execute()

        labels_list = [row['name'] for row in labels_list['labels'] if 'labelListVisibility' in row]

        return labels_list

    def move_email_message(self, message_id, updated_message):
        """
        method to move the message to given folder
        :param message_id:
        :param updated_message:
        :return:
        """

        self.service.users().messages().modify(userId='me', id=message_id, body=updated_message).execute()
