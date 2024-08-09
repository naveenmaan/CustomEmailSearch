from datetime import datetime
from lib.base.base_entity import BaseEntity


class EmailEntity(BaseEntity):

    def __init__(self, email_details):
        """
        method to init the required resources
        """

        self.__email_id = None
        self.__message_id = None
        self.__thread_id = None
        self.__subject = None
        self.__from_address = None
        self.__to_addresses = None
        self.__cc_addresses = None
        self.__bcc_addresses = None
        self.__reply_address = None
        self.__received_date = None
        self.__labels = None
        self.__body = None
        self.__created_datetime = datetime.now()
        self.__created_by = None
        self.__modified_datetime = None
        self.__modified_by = None

        self.assign_values(email_details)

    @property
    def email_id(self):
        return self.__email_id

    @email_id.setter
    def email_id(self, email_id):
        self.__email_id = email_id

    @property
    def message_id(self):
        return self.__message_id

    @message_id.setter
    def message_id(self, message_id):
        self.__message_id = message_id

    @property
    def thread_id(self):
        return self.__thread_id

    @thread_id.setter
    def thread_id(self, thread_id):
        self.__thread_id = thread_id

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self, subject):
        self.__subject = subject.encode('ascii', 'ignore').strip()

    @property
    def from_address(self):
        return self.__from_address

    @from_address.setter
    def from_address(self, from_address):
        self.__from_address = from_address

    @property
    def to_addresses(self):
        return self.__to_addresses

    @to_addresses.setter
    def to_addresses(self, to_addresses):
        self.__to_addresses = to_addresses

    @property
    def cc_addresses(self):
        return self.__cc_addresses

    @cc_addresses.setter
    def cc_addresses(self, cc_addresses):
        self.__cc_addresses = cc_addresses

    @property
    def bcc_addresses(self):
        return self.__bcc_addresses

    @bcc_addresses.setter
    def bcc_addresses(self, bcc_addresses):
        self.__bcc_addresses = bcc_addresses

    @property
    def reply_address(self):
        return self.__reply_address

    @reply_address.setter
    def reply_address(self, reply_address):
        self.__reply_address = reply_address

    @property
    def received_date(self):
        return self.__received_date

    @received_date.setter
    def received_date(self, received_date):
        if isinstance(received_date, str):
            received_date = datetime.strptime(received_date, "%a, %d %b %Y %H:%M:%S %z")
        self.__received_date = received_date

    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, labels):
        self.__labels = labels

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, body):
        self.__body = body.encode('ascii', 'ignore')

    @property
    def created_datetime(self):
        return self.__created_datetime

    @created_datetime.setter
    def created_datetime(self, created_datetime):
        self.__created_datetime = created_datetime

    @property
    def created_by(self):
        return self.__created_by

    @created_by.setter
    def created_by(self, created_by):
        self.__created_by = created_by

    @property
    def modified_datetime(self):
        return self.__modified_datetime

    @modified_datetime.setter
    def modified_datetime(self, modified_datetime):
        self.__modified_datetime = modified_datetime

    @property
    def modified_by(self):
        return self.__modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        self.__modified_by = modified_by
