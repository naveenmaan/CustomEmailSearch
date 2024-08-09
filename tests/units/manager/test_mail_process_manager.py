import json
import pytest
import datetime

from lib.custom_exception import DBConnectionError
from src.entity.email_entity import EmailEntity
from src.dao.communication_dao import CommunicationDAO
from src.manager.mail_process_manager import MailProcessManager


class MockedMySqlDBManager:

    def __init__(self, connection_name):
        ...


    def run_query(self, query, arguments=None, fetch=False, count=0, primary_key=False):
        ...

    def save(self):
        ...

    def end(self):
        ...

    def rollback(self):
        ...


class MockedGmailManager:

    def move_email_message(self, message_id, updated_message):
        ...

    def get_user_label_list(self):
        return ['INBOX', 'IMPORTANT']

    def get_unread_email(self):
        ...

    def get_email_detail(self, message_id):
        response = {
            "123": {
            'id': '123',
            'threadId': 'we23423234',
            'labelIds': [
                'SENT'
            ],
            'snippet': 'test',
            'payload': {
                'partId': '',
                'mimeType': 'multipart/alternative',
                'filename': '',
                'headers': [
                    {
                        'name': 'MIME-Version',
                        'value': '1.0'
                    },
                    {
                        'name': 'Received',
                        'value': 'by 2002:a17:907:9706:0:0:0:0 with HTTP; Sat, 27 Nov 2021 04:55:40 -0800 (PST)'
                    },
                    {
                        'name': 'In-Reply-To',
                        'value': '<CsfdsLzFWw@mail.gmail.com>'
                    },
                    {
                        'name': 'References',
                        'value': '<sdfsdfWw@mail.gmail.com>'
                    },
                    {
                        'name': 'Date',
                        'value': 'Sat, 27 Nov 2021 18:25:40 +0530'
                    },
                    {
                        'name': 'Delivered-To',
                        'value': 'm***@gmail.com'
                    },
                    {
                        'name': 'Message-ID',
                        'value': '<CsdfsdmUAOgg@mail.gmail.com>'
                    },
                    {
                        'name': 'Subject',
                        'value': 'Fwd: TEst'
                    },
                    {
                        'name': 'From',
                        'value': 'test <m***@gmail.com>'
                    },
                    {
                        'name': 'To',
                        'value': 'test <m***@gmail.com>'
                    },
                    {
                        'name': 'Content-Type',
                        'value': 'multipart/alternative; boundary="0000000000008ea94305d1c4b988"'
                    }
                ],
                'body': {
                    'size': 0
                },
                'parts': [
                    {
                        'partId': '0',
                        'mimeType': 'text/plain',
                        'filename': '',
                        'headers': [
                            {
                                'name': 'Content-Type',
                                'value': 'text/plain; charset="UTF-8"'
                            }
                        ],
                        'body': {
                            'size': 3866,
                            'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                        }
                    },
                    {
                        'partId': '1',
                        'mimeType': 'text/html',
                        'filename': '',
                        'headers': [
                            {
                                'name': 'Content-Type',
                                'value': 'text/html; charset="UTF-8"'
                            },
                            {
                                'name': 'Content-Transfer-Encoding',
                                'value': 'quoted-printable'
                            }
                        ],
                        'body': {
                            'size': 8803,
                            'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                        }
                    }
                ]
            },
            'sizeEstimate': 14139,
            'historyId': '180905',
            'internalDate': '1638017740000'
            }
        }

        return response[message_id]


def mock_open(filename, mode):
    return MockFile(json.dumps({"rule_name": {"category": "all",
                            "conditions": [{"field": "from", "operator": "contains", "value": "test@gmail.com"}],
                            "action": [{"type": "move", "value": "Inbox"}, {"type": "read"}]}}))

class MockFile:
    def __init__(self, content):
        self.content = content
    def read(self):
        return self.content
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestMailProcessManager:

    def test_get_email_by_id(self, monkeypatch):
        """method to test the get_email_by_id functionality"""

        monkeypatch.setattr("src.manager.mail_process_manager.MySqlDBManager", MockedMySqlDBManager)
        monkeypatch.setattr("src.manager.mail_process_manager.GMailManager", MockedGmailManager)

        output = MailProcessManager().get_email_by_id("123")

        expected_result = {'email_id': None, 'message_id': '123',
                           'thread_id': 'we23423234', 'subject': b'Fwd: TEst',
                           'from_address': 'test <m***@gmail.com>',
                           'to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,
                           'bcc_addresses': None, 'reply_address': None,
                           'received_date': datetime.datetime(2021, 11, 27, 18, 25, 40, tzinfo=datetime.timezone( datetime.timedelta(seconds=19800))),
                           'labels': 'SENT', 'body': b'this is a test message',
                           'created_by': 'EMAIL_PROCESSING_MANAGER',
                           'modified_datetime': None, 'modified_by': None}

        for key, value in expected_result.items():
            assert value == getattr(output, key)

    @pytest.mark.parametrize(
        "input, exception",
        [([{
        'id': '123',
        'threadId': 'we23423234',
        'labelIds': [
            'SENT'
        ],
        'snippet': 'test',
        'payload': {
            'partId': '',
            'mimeType': 'multipart/alternative',
            'filename': '',
            'headers': [
                {
                    'name': 'MIME-Version',
                    'value': '1.0'
                },
                {
                    'name': 'Received',
                    'value': 'by 2002:a17:907:9706:0:0:0:0 with HTTP; Sat, 27 Nov 2021 04:55:40 -0800 (PST)'
                },
                {
                    'name': 'In-Reply-To',
                    'value': '<CsfdsLzFWw@mail.gmail.com>'
                },
                {
                    'name': 'References',
                    'value': '<sdfsdfWw@mail.gmail.com>'
                },
                {
                    'name': 'Date',
                    'value': 'Sat, 27 Nov 2021 18:25:40 +0530'
                },
                {
                    'name': 'Delivered-To',
                    'value': 'm***@gmail.com'
                },
                {
                    'name': 'Message-ID',
                    'value': '<CsdfsdmUAOgg@mail.gmail.com>'
                },
                {
                    'name': 'Subject',
                    'value': 'Fwd: TEst'
                },
                {
                    'name': 'From',
                    'value': 'test <m***@gmail.com>'
                },
                {
                    'name': 'To',
                    'value': 'test <m***@gmail.com>'
                },
                {
                    'name': 'Content-Type',
                    'value': 'multipart/alternative; boundary="0000000000008ea94305d1c4b988"'
                }
            ],
            'body': {
                'size': 0
            },
            'parts': [
                {
                    'partId': '0',
                    'mimeType': 'text/plain',
                    'filename': '',
                    'headers': [
                        {
                            'name': 'Content-Type',
                            'value': 'text/plain; charset="UTF-8"'
                        }
                    ],
                    'body': {
                        'size': 3866,
                        'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                    }
                },
                {
                    'partId': '1',
                    'mimeType': 'text/html',
                    'filename': '',
                    'headers': [
                        {
                            'name': 'Content-Type',
                            'value': 'text/html; charset="UTF-8"'
                        },
                        {
                            'name': 'Content-Transfer-Encoding',
                            'value': 'quoted-printable'
                        }
                    ],
                    'body': {
                        'size': 8803,
                        'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                    }
                }
            ]
        },
        'sizeEstimate': 14139,
        'historyId': '180905',
        'internalDate': '1638017740000'
    }], 0),
        (None, 1)]
    )
    def test_get_latest_email(self, monkeypatch, input, exception):
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr("src.manager.mail_process_manager.MySqlDBManager", MockedMySqlDBManager)
        monkeypatch.setattr("src.manager.mail_process_manager.GMailManager", MockedGmailManager)

        def mock_get_unread_email(self):
            if exception:
                raise Exception("This is an exception")
            return input

        monkeypatch.setattr(MockedGmailManager, "get_unread_email", mock_get_unread_email)

        if exception:
            assert None == MailProcessManager().get_latest_email()
        else:
            output = MailProcessManager().get_latest_email()
            assert output == input

    @pytest.mark.parametrize(
        "input, expected_output, exception",
        [
            ([{'id': '123'}], [], False),
            ([{'id': '1234'}], [], False),
            ([{'id': '1234'}], ['1234'], True),
        ]
    )
    def test_store_email_details(self, monkeypatch, input, expected_output, exception):
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr("src.manager.mail_process_manager.MySqlDBManager", MockedMySqlDBManager)
        monkeypatch.setattr("src.manager.mail_process_manager.GMailManager", MockedGmailManager)

        def mock_get_message_by_id(self, message_id):
            response = {
                '123': "test",
            }

            return response.get(message_id)

        def mock_insert_email_details(self, email_entity_obj):
            if exception:
                raise Exception("Unkown exception")

        def mock_get_email_detail(self, message_id):
            return {
            'id': '123',
            'threadId': 'we23423234',
            'labelIds': [
                'SENT'
            ],
            'snippet': 'test',
            'payload': {
                'partId': '',
                'mimeType': 'multipart/alternative',
                'filename': '',
                'headers': [
                    {
                        'name': 'MIME-Version',
                        'value': '1.0'
                    },
                    {
                        'name': 'Received',
                        'value': 'by 2002:a17:907:9706:0:0:0:0 with HTTP; Sat, 27 Nov 2021 04:55:40 -0800 (PST)'
                    },
                    {
                        'name': 'In-Reply-To',
                        'value': '<CsfdsLzFWw@mail.gmail.com>'
                    },
                    {
                        'name': 'References',
                        'value': '<sdfsdfWw@mail.gmail.com>'
                    },
                    {
                        'name': 'Date',
                        'value': 'Sat, 27 Nov 2021 18:25:40 +0530'
                    },
                    {
                        'name': 'Delivered-To',
                        'value': 'm***@gmail.com'
                    },
                    {
                        'name': 'Message-ID',
                        'value': '<CsdfsdmUAOgg@mail.gmail.com>'
                    },
                    {
                        'name': 'Subject',
                        'value': 'Fwd: TEst'
                    },
                    {
                        'name': 'From',
                        'value': 'test <m***@gmail.com>'
                    },
                    {
                        'name': 'To',
                        'value': 'test <m***@gmail.com>'
                    },
                    {
                        'name': 'Content-Type',
                        'value': 'multipart/alternative; boundary="0000000000008ea94305d1c4b988"'
                    }
                ],
                'body': {
                    'size': 0
                },
                'parts': [
                    {
                        'partId': '0',
                        'mimeType': 'text/plain',
                        'filename': '',
                        'headers': [
                            {
                                'name': 'Content-Type',
                                'value': 'text/plain; charset="UTF-8"'
                            }
                        ],
                        'body': {
                            'size': 3866,
                            'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                        }
                    },
                    {
                        'partId': '1',
                        'mimeType': 'text/html',
                        'filename': '',
                        'headers': [
                            {
                                'name': 'Content-Type',
                                'value': 'text/html; charset="UTF-8"'
                            },
                            {
                                'name': 'Content-Transfer-Encoding',
                                'value': 'quoted-printable'
                            }
                        ],
                        'body': {
                            'size': 8803,
                            'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                        }
                    }
                ]
            },
            'sizeEstimate': 14139,
            'historyId': '180905',
            'internalDate': '1638017740000'
            }

        monkeypatch.setattr(MockedGmailManager, "get_email_detail", mock_get_email_detail)

        monkeypatch.setattr(CommunicationDAO, "get_message_by_id", mock_get_message_by_id)
        monkeypatch.setattr(CommunicationDAO, "insert_email_details", mock_insert_email_details)

        output = MailProcessManager().store_email_details(input)

        assert output == expected_output

    @pytest.mark.parametrize(
        "input, filter_items, expected_output, exception",
        [
            ("rule_s", [], [], False),
            ("rule_name", [], None, False),
            ("rule_name", [EmailEntity({'email_id': None, 'message_id': '123','thread_id': 'we23423234', 'subject': 'Fwd: TEst','from_address': 'test <m***@gmail.com>','to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,'bcc_addresses': None, 'reply_address': None,'received_date': datetime.datetime(2021, 11, 27, 18, 25, 40, tzinfo=datetime.timezone( datetime.timedelta(seconds=19800))),'labels': 'SENT,INBOX,READ', 'body': 'this is a test message','created_by': 'EMAIL_PROCESSING_MANAGER','modified_datetime': None, 'modified_by': None})], None, None),
            ("rule_name", [EmailEntity({'email_id': None, 'message_id': '123','thread_id': 'we23423234', 'subject': 'Fwd: TEst','from_address': 'test <m***@gmail.com>','to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,'bcc_addresses': None, 'reply_address': None,'received_date': datetime.datetime(2021, 11, 27, 18, 25, 40, tzinfo=datetime.timezone( datetime.timedelta(seconds=19800))),'labels': 'SENT,IMPORTANT', 'body': 'this is a test message','created_by': 'EMAIL_PROCESSING_MANAGER','modified_datetime': None, 'modified_by': None})], None, None),
            ("rule_name", [EmailEntity({'email_id': None, 'message_id': '123','thread_id': 'we23423234', 'subject': 'Fwd: TEst','from_address': 'test <m***@gmail.com>','to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,'bcc_addresses': None, 'reply_address': None,'received_date': datetime.datetime(2021, 11, 27, 18, 25, 40, tzinfo=datetime.timezone( datetime.timedelta(seconds=19800))),'labels': 'SENT,IMPORTANT', 'body': 'this is a test message','created_by': 'EMAIL_PROCESSING_MANAGER','modified_datetime': None, 'modified_by': None})], None, Exception),
            ("rule_name", [EmailEntity({'email_id': None, 'message_id': '123','thread_id': 'we23423234', 'subject': 'Fwd: TEst','from_address': 'test <m***@gmail.com>','to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,'bcc_addresses': None, 'reply_address': None,'received_date': datetime.datetime(2021, 11, 27, 18, 25, 40, tzinfo=datetime.timezone( datetime.timedelta(seconds=19800))),'labels': 'SENT,IMPORTANT', 'body': 'this is a test message','created_by': 'EMAIL_PROCESSING_MANAGER','modified_datetime': None, 'modified_by': None})], None, DBConnectionError),
        ]
    )
    def test_execute_rule_by_rule_name(self, monkeypatch, input, filter_items, expected_output, exception):
        monkeypatch.setattr("builtins.open", mock_open)
        monkeypatch.setattr("src.manager.mail_process_manager.MySqlDBManager", MockedMySqlDBManager)
        monkeypatch.setattr("src.manager.mail_process_manager.GMailManager", MockedGmailManager)

        def mock_get_filtered_by_given_condition(self, filter_logic):
            return filter_items

        def mock_insert_action_event(self, action_details):
            return 123

        def mock_update_message_label(self, email_entity_obj):
            if exception:
                assert email_entity_obj['status'] == "FAILURE"

        def mock_update_message_label(self, email_entity_obj):
            if exception:
                raise exception("Test")

        def mock_get_email_detail(self, message_id):
            return {
                'id': '123',
                'threadId': 'we23423234',
                'labelIds': [
                    'SENT'
                ],
                'snippet': 'test',
                'payload': {
                    'partId': '',
                    'mimeType': 'multipart/alternative',
                    'filename': '',
                    'headers': [
                        {
                            'name': 'MIME-Version',
                            'value': '1.0'
                        },
                        {
                            'name': 'Received',
                            'value': 'by 2002:a17:907:9706:0:0:0:0 with HTTP; Sat, 27 Nov 2021 04:55:40 -0800 (PST)'
                        },
                        {
                            'name': 'In-Reply-To',
                            'value': '<CsfdsLzFWw@mail.gmail.com>'
                        },
                        {
                            'name': 'References',
                            'value': '<sdfsdfWw@mail.gmail.com>'
                        },
                        {
                            'name': 'Date',
                            'value': 'Sat, 27 Nov 2021 18:25:40 +0530'
                        },
                        {
                            'name': 'Delivered-To',
                            'value': 'm***@gmail.com'
                        },
                        {
                            'name': 'Message-ID',
                            'value': '<CsdfsdmUAOgg@mail.gmail.com>'
                        },
                        {
                            'name': 'Subject',
                            'value': 'Fwd: TEst'
                        },
                        {
                            'name': 'From',
                            'value': 'test <m***@gmail.com>'
                        },
                        {
                            'name': 'To',
                            'value': 'test <m***@gmail.com>'
                        },
                        {
                            'name': 'Content-Type',
                            'value': 'multipart/alternative; boundary="0000000000008ea94305d1c4b988"'
                        }
                    ],
                    'body': {
                        'size': 0
                    },
                    'parts': [
                        {
                            'partId': '0',
                            'mimeType': 'text/plain',
                            'filename': '',
                            'headers': [
                                {
                                    'name': 'Content-Type',
                                    'value': 'text/plain; charset="UTF-8"'
                                }
                            ],
                            'body': {
                                'size': 3866,
                                'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                            }
                        },
                        {
                            'partId': '1',
                            'mimeType': 'text/html',
                            'filename': '',
                            'headers': [
                                {
                                    'name': 'Content-Type',
                                    'value': 'text/html; charset="UTF-8"'
                                },
                                {
                                    'name': 'Content-Transfer-Encoding',
                                    'value': 'quoted-printable'
                                }
                            ],
                            'body': {
                                'size': 8803,
                                'data': 'dGhpcyBpcyBhIHRlc3QgbWVzc2FnZQ=='
                            }
                        }
                    ]
                },
                'sizeEstimate': 14139,
                'historyId': '180905',
                'internalDate': '1638017740000'
            }

        monkeypatch.setattr(MockedGmailManager, "get_email_detail", mock_get_email_detail)

        monkeypatch.setattr(CommunicationDAO, "get_filtered_by_given_condition", mock_get_filtered_by_given_condition)
        monkeypatch.setattr(CommunicationDAO, "insert_action_event", mock_insert_action_event)
        monkeypatch.setattr(CommunicationDAO, "update_message_label", mock_update_message_label)
        monkeypatch.setattr(CommunicationDAO, "update_message_label", mock_update_message_label)

        output = MailProcessManager().execute_rule_by_rule_name(input)
        assert output == expected_output
