from lib.db.MySqlDBManager import MySqlDBManager
from lib.email.gmail_manager import GMailManager
from lib.custom_exception import DBConnectionError, DBQueryError, DBException

from src.config.email_config import CREATED_BY
from src.config.rule_config import REVERSE_MAPPING, UNREAD
from src.utils.utils import format_email_entity
from src.manager.rule_engine_manager import RuleEngineManager
from src.dao.communication_dao import CommunicationDAO


class MailProcessManager:

    def __init__(self):
        """
        method to init the required resources
        """

        self.db_conn = MySqlDBManager("COMMUNICATION")
        self.comm_dao_obj = CommunicationDAO(self.db_conn)
        self.email_manager = GMailManager()
        self.rule_engine_manager_obj = RuleEngineManager()
        self.label_list = []

    def get_email_by_id(self, message_id):
        """
        method to get the email from the mailbox by message id
        :param message_id: 1236
        :return:EmailEntity
        """

        email_details = self.email_manager.get_email_detail(message_id)
        email_details['created_by'] = CREATED_BY
        email_entity_obj = format_email_entity(email_details)

        return email_entity_obj

    def get_latest_email(self):
        """
        method to fetch the latest mail from and store the database
        :return:
        """
        try:
            messages = self.email_manager.get_unread_email()
            return messages
        except Exception as ex:
            print(ex)

    def store_email_details(self, messages):
        """
        method to store the fetched emails
        :param messages: [{'id' : '1332'}]
        :return: ['1332']
        """

        failure_list = []

        for row in messages:
            try:
                print(f"Processing message {row['id']}")
                email_details = self.comm_dao_obj.get_message_by_id(row['id'])
                if email_details:
                    continue

                email_details = self.get_email_by_id(row['id'])
                self.comm_dao_obj.insert_email_details(email_details)
                self.db_conn.save()
            except Exception as ex:
                    print(ex)
                    failure_list.append(row['id'])

        self.db_conn.end()

        return failure_list

    def get_filtered_email_list_by_rule_detail(self, rule_detail_entity_obj):
        """
        method to get the filtered emails based on the rules details
        :param rule_detail_entity_obj: RuleDetailEntity
        :return: [EmailEntity]
        """

        message_list = []

        query_condition = self.rule_engine_manager_obj.email_query_build_by_rule(rule_detail_entity_obj)
        message_list = self.comm_dao_obj.get_filtered_by_given_condition(query_condition)

        return message_list

    def __update_label_based_on_action(self, email_entity_obj, action_entity_obj):
        """
        method to return the updated label if required to change
        :param email_entity_obj: EmailEntity
        :param action_entity_obj: RuleActionEntity
        :return: False/ [Read,CATEGORY_UPDATES,INBOX]
        """

        email_labels = email_entity_obj.labels.split(",")
        updated_message = {'addLabelIds': [], 'removeLabelIds': []}

        # folder remove list
        remove_list = [row for row in email_labels if row in self.label_list]

        for action in action_entity_obj:
            if action.value and action.value.upper() in email_labels:
                continue

            if action.type.upper() in email_labels:
                continue

            if action.value:
                add_label = action.value.upper()
                updated_message['addLabelIds'].append(add_label)

            if action.value and len(updated_message['removeLabelIds'])==0:
                updated_message['removeLabelIds'] += remove_list

            if not action.value:
                updated_message['removeLabelIds'].append(REVERSE_MAPPING.get(action.type).upper())

        updated_labels = [row for row in email_labels if row not in updated_message['removeLabelIds']]
        updated_labels.extend(updated_message['addLabelIds'])
        email_entity_obj.labels = ",".join(updated_labels)

        return updated_message

    def messages_action_perforation(self, action_entity_obj, message_list):
        """
        method to perform the given action on the message list
        :param action_entity_obj: RuleActionEntity
        :param message_list: [EmailEntity]
        :return:
        """

        if not self.label_list:
            self.label_list = self.email_manager.get_user_label_list()

        if not message_list:
            print("No Message to perform given action")
            return

        for message in message_list:
            print(f"Processing email_id: {message.email_id}")
            action_obj = {
                "action_history_id": None,
                "email_id": message.email_id,
                "action_type": None,
                "additional_details": None,
                "status": "NEW",
                "failure_reason": "",
                "created_by": CREATED_BY
            }
            try:
                updated_message = self.__update_label_based_on_action(message, action_entity_obj)
                if len(updated_message['addLabelIds'])==0:
                    continue

                action_history_id = self.comm_dao_obj.insert_action_event(action_obj)
                action_obj['action_history_id'] = action_history_id

                self.email_manager.move_email_message(message.message_id, updated_message)

                message.modified_by = CREATED_BY
                self.comm_dao_obj.update_message_label(message)
                action_obj['modified_by'] = CREATED_BY
                action_obj['status'] = 'SUCCESS'
                self.comm_dao_obj.update_action_statu_event(action_obj)
            except (DBConnectionError, DBQueryError, DBException) as ex:
                self.db_conn.rollback()
                print(f"{ex} exception occurred")
            except Exception as ex:
                if action_obj['action_history_id']:
                    action_obj['modified_by'] = CREATED_BY
                    action_obj['status'] = 'FAILURE'
                    action_obj['failure_reason'] = ex
                    self.comm_dao_obj.update_action_statu_event(action_obj)
                print(f"{ex} exception occurred")
            finally:
                self.db_conn.save()

    def execute_rule_by_rule_name(self, rule_name):
        """
        method to perform the rule actions on required emails based on the given rule name
        :param rule_name: test
        :return:
        """

        rule_detail_entity_obj = self.rule_engine_manager_obj.get_rule_by_name(rule_name)

        if rule_detail_entity_obj is None:
            print("Rule Does not exist")
            return []

        message_list = self.get_filtered_email_list_by_rule_detail(rule_detail_entity_obj)

        self.messages_action_perforation(rule_detail_entity_obj.action, message_list)
