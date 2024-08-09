import datetime
from src.entity.email_entity import EmailEntity


class TestEmailEntity:

    def test_entity(self):
        input = {'email_id': None, 'message_id': '123',
                           'thread_id': 'we23423234', 'subject': 'Fwd: TEst',
                           'from_address': 'test <m***@gmail.com>',
                           'to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,
                           'bcc_addresses': None, 'reply_address': None,
                           'received_date': 'Sat, 27 Nov 2021 18:25:40 +0530',
                           'labels': 'SENT', 'body': 'this is a test message',
                            'created_datetime': None,
                           'modified_datetime': None, 'modified_by': None,
                           'created_by': 'EMAIL_PROCESSING_MANAGER',}

        expected_result = {'email_id': None, 'message_id': '123',
                           'thread_id': 'we23423234', 'subject': b'Fwd: TEst',
                           'from_address': 'test <m***@gmail.com>',
                           'to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,
                           'bcc_addresses': None, 'reply_address': None,
                           'received_date': datetime.datetime(2021, 11, 27, 18, 25, 40, tzinfo=datetime.timezone(
                               datetime.timedelta(seconds=19800))),
                           'labels': 'SENT', 'body': b'this is a test message',
                           'created_by': 'EMAIL_PROCESSING_MANAGER',
                           'created_datetime': None,
                           'modified_datetime': None, 'modified_by': None}

        output = EmailEntity(input)

        for key, value in expected_result.items():
            assert value == getattr(output, key)