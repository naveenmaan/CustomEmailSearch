import datetime
from src.utils.utils import format_email_entity


def test_format_email_entity():

    output = format_email_entity({
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
            'internalDate': '1638017740000',
            "created_by": 'EMAIL_PROCESSING_MANAGER'
            })

    expected_result = {'email_id': None, 'message_id': '123',
                       'thread_id': 'we23423234', 'subject': b'Fwd: TEst',
                       'from_address': 'test <m***@gmail.com>',
                       'to_addresses': 'test <m***@gmail.com>', 'cc_addresses': None,
                       'bcc_addresses': None, 'reply_address': None,
                       'received_date': datetime.datetime(2021, 11, 27, 18, 25, 40,
                                                          tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))),
                       'labels': 'SENT', 'body': b'this is a test message',
                       'created_by': 'EMAIL_PROCESSING_MANAGER',
                       'modified_datetime': None, 'modified_by': None}

    for key, value in expected_result.items():
        assert value == getattr(output, key)