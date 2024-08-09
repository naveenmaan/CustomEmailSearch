from lib.custom_exception import DBConnectionError, DBQueryError, DBException
from src.entity.email_entity import EmailEntity


class CommunicationDAO:

    def __init__(self, db_conn):
        """
        init the required resources for the dao
        :param db_conn:
        """

        self.db_conn = db_conn

    def insert_email_details(self, email_entity_obj):
        """
        method to store the email details
        :param email_entity_obj: EmailEntity
        :return:
        """

        try:
            query = ("insert into email (message_id, thread_id, subject, from_address,"
                     " to_addresses, cc_addresses, bcc_addresses, reply_address,"
                     " received_date, labels, body, created_datetime, created_by)"
                     " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            arguments = [email_entity_obj.message_id, email_entity_obj.thread_id, email_entity_obj.subject,
                         email_entity_obj.from_address, email_entity_obj.to_addresses, email_entity_obj.cc_addresses,
                         email_entity_obj.bcc_addresses, email_entity_obj.reply_address, email_entity_obj.received_date,
                         email_entity_obj.labels, email_entity_obj.body, email_entity_obj.created_datetime,
                         email_entity_obj.created_by]

            email_id = self.db_conn.run_query(query, arguments, primary_key=True)

            return email_id

        except (DBConnectionError, DBQueryError, DBException) as ex:
            print("Exception occurred in database")
            raise ex
        except Exception as ex:
            print("Unexpected error occurred")
            raise ex

    def update_message_label(self, email_entity_obj):
        """
        method to update the message labels
        :param email_entity_obj: EmailEntity
        :return:
        """

        try:
            query = "update email set labels=%s,modified_datetime=now(),modified_by=%s where email_id=%s"
            arguments = [email_entity_obj.labels,
                         email_entity_obj.modified_by,
                         email_entity_obj.email_id]

            self.db_conn.run_query(query, arguments)
        except (DBConnectionError, DBQueryError, DBException) as ex:
            print("Exception occurred in database")
            raise ex
        except Exception as ex:
            print("Unexpected error occurred")
            raise ex

    def get_filtered_by_given_condition(self, filter_logic):
        """
        method to get the email based on the given filter
        :param filter_logic: "from like '%test%'"
        :return:
        """

        try:
            query = "select * from email where %s" %filter_logic

            emails_result = self.db_conn.run_query(query, fetch=True)
            output = []

            for row in emails_result:
                output.append(EmailEntity(row))

            return output
        except (DBConnectionError, DBQueryError, DBException) as ex:
            print("Exception occurred in database")
            raise ex
        except Exception as ex:
            print("Unexpected error occurred")
            raise ex

    def get_message_by_id(self, message_id):
        """
        method to get the message by id
        :param message_id: 1232
        :return: [EmailEntity]
        """
        try:
            query = "select * from email where message_id = %s"
            arguments = [message_id]

            emails_result = self.db_conn.run_query(query, arguments, fetch=True)
            output = []

            for row in emails_result:
                output.append(EmailEntity(row))

            return output
        except (DBConnectionError, DBQueryError, DBException) as ex:
            print("Exception occurred in database")
            raise ex
        except Exception as ex:
            print("Unexpected error occurred")
            raise ex
    def insert_action_event(self, action_details):
        """
        method to insert action event in system
        :param action_details:
        :return: 1232
        """

        try:
            query = "insert into action_history(email_id, action_type, additional_details, status) values(%s, %s, %s, %s)"
            arguments = [action_details['email_id'],
                         action_details['action_type'],
                         action_details['additional_details'],
                         action_details['status']]

            action_history_id = self.db_conn.run_query(query, arguments, primary_key=True)
            return action_history_id
        except (DBConnectionError, DBQueryError, DBException) as ex:
            print("Exception occurred in database")
            raise ex
        except Exception as ex:
            print("Unexpected error occurred")
            raise ex

    def update_action_statu_event(self, action_details):
        """
        method to insert action event in system
        :param action_details:
        :return:
        """

        try:
            query = "update action_history set status=%s,failure_reason=%s,modified_datetime=now(),modified_by=%s where action_history_id=%s"
            arguments = [action_details['status'],
                         action_details['failure_reason'],
                         action_details['modified_by'],
                         action_details['action_history_id']]

            self.db_conn.run_query(query, arguments)
        except (DBConnectionError, DBQueryError, DBException) as ex:
            print("Exception occurred in database")
            raise ex
        except Exception as ex:
            print("Unexpected error occurred")
            raise ex