import json
from lib.custom_exception import ValidationException
from src.config.rule_config import RULES_FILE_LOCATION, OPERATOR_MAPPING, FILED_MAPPING, CATEGORY_MAPPING, STRING_FIELDS
from src.entity.rule_entity import RuleDetailEntity


class RuleEngineManager:

    def __init__(self):
        """init the required resources"""

        self.__rules_list_details = {}
        self.get_rules_list()

    def get_rules_list(self):
        """
        method to read the rules file and load in rules list
        :return:
        """

        try:
            with open(RULES_FILE_LOCATION, "r") as rules_file_obj:
                rules_list_details = json.loads(rules_file_obj.read())

            for key, value in rules_list_details.items():
                self.__rules_list_details[key] = RuleDetailEntity(value)
        except FileNotFoundError as ex:
            print("Rule file not found")
            raise ex
        except ValidationException as ex:
            print("Some rule has un-wanted value")
            raise ex

    def get_rule_by_name(self, rule_name):
        """
        method to get the rule details for the given rule name
        :param rule_name: move to inbox
        :return:
        """

        return self.__rules_list_details.get(rule_name)

    def __get_string_query(self, condition):
        """
        method to return the string query based on the given condition
        :param condition: RuleConditionEntity
        :return: "from rlike 'test'"
        """

        field = FILED_MAPPING.get(condition.field)
        operator = OPERATOR_MAPPING.get(condition.operator)

        query = f"{field} {operator} '{condition.value}'"
        return query

    def __get_datetime_query(self, condition):
        """
        method to get the date related queries
        :param condition:
        :return:
        """

        field = FILED_MAPPING.get(condition.field)
        operator = OPERATOR_MAPPING.get(condition.operator)
        value = condition.value

        query = f"{field} {operator} curdate() - interval {value} {condition.duration_type}"
        return query

    def email_query_build_by_rule(self, rule_detail_entity_obj):
        """
        method to build the search query based on given rule detail
        :param rule_detail_entity_obj: RuleDetailEntity
        :return: "from like '%test%'"
        """

        condition_operation = CATEGORY_MAPPING.get(rule_detail_entity_obj.category)

        query = []

        query_type_mapping = {
            True: self.__get_string_query,
            False: self.__get_datetime_query
        }

        for condition in rule_detail_entity_obj.conditions:
            is_string_filed = True if condition.field in STRING_FIELDS else False
            query.append(query_type_mapping[is_string_filed](condition))

        query = condition_operation.join(query)

        return query
