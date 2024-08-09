import base64
from bs4 import BeautifulSoup
from src.config.email_config import GMAIL_HEADER_MAPPER
from src.entity.email_entity import EmailEntity


def format_email_entity(email_content):
    """
    method to format the email content received from gmail and convert into Email Entity
    :param email_content:
        {
            'id': 'sdfw23',
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
                            'data': 'sdfsd'
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
                            'data': 'sdfsd'
                        }
                    }
                ]
            },
            'sizeEstimate': 14139,
            'historyId': '180905',
            'internalDate': '1638017740000'
            }
    :return: EmailEntity()
    """

    # decoding the body test
    decoded_data = base64.b64decode(email_content['payload']['parts'][0]['body']['data'].replace("-","+").replace("_","/"))
    soup = BeautifulSoup(decoded_data, "lxml")
    body = soup.body()[0]

    # email dict
    email_dict = {
        "message_id": email_content['id'],
        "thread_id": email_content['threadId'],
        "subject": None,
        "from_address": None,
        "to_addresses": None,
        "cc_addresses": None,
        "bcc_addresses": None,
        "reply_address": None,
        "received_date": None,
        "labels": ",".join(email_content['labelIds']),
        "created_by": email_content['created_by'],
        "body": body.text,
    }

    for row in email_content['payload']['headers']:
        if row['name'] in GMAIL_HEADER_MAPPER:
            email_dict[GMAIL_HEADER_MAPPER[row['name']]] = row['value']

    email_entity_obj = EmailEntity(email_dict)

    return email_entity_obj
