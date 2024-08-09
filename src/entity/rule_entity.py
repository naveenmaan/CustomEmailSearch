from lib.decorator.validator import validator
from lib.custom_exception import ValidationException
from lib.base.base_entity import BaseEntity
from src.config.rule_config import VALIDATION, COMBINATION_MAPPING


class RuleConditionEntity(BaseEntity):

    def __init__(self, condition_details):
        """
        method to init the condition details
        :param condition_details: {
            "field": "From",
            "operator": "Contains",
            "value": 'test@gmail.com'
        }
        """

        self.__field = None
        self.__operator = None
        self.__value = None
        self.__duration_type = None

        self.assign_values(condition_details)

    def validate_combination(self, field, operator):
        """
        method to check the condition combination
        :param field: FROM
        :param operator: CONTAINS
        :return:
        """

        for field_category, operator_category in COMBINATION_MAPPING.items():
            if (field in field_category)!= (operator in operator_category):
                raise ValidationException(f"{field} is not applicable for {operator} category")

    @property
    def field(self):
        return self.__field

    @field.setter
    @validator(VALIDATION['field'])
    def field(self, field):
        if self.operator:
            self.validate_combination(field, self.operator)
        self.__field = field

    @property
    def operator(self):
        return self.__operator

    @operator.setter
    @validator(VALIDATION['operator'])
    def operator(self, operator):
        if self.field:
            self.validate_combination(self.field, operator)
        self.__operator = operator

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def duration_type(self):
        return self.__duration_type

    @duration_type.setter
    @validator(VALIDATION['duration_type'])
    def duration_type(self, duration_type):
        self.__duration_type = duration_type


class RuleActionEntity(BaseEntity):

    def __init__(self, action_details):
        """
        method to init the action entity with the details
        :param action_details:
            {
                "category": "read",
            }
        """

        self.__category = None
        self.__value = None

        self.assign_values(action_details)

    @property
    def category(self):
        return self.__category

    @category.setter
    @validator(VALIDATION['action_category'])
    def category(self, category):
        self.__category = category

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class RuleDetailEntity(BaseEntity):

    def __init__(self, rule_details):
        """
        method to init the rule entity
        :param rule_details:
            {
                "category": "All",
                "condition": [
                    {
                        "field": "From",
                        "operator": "Contains",
                        "value": 'test@gmail.com'
                    }
                ],
                "actions": [
                    {
                        "category": "read",
                    }
                ]
            }
        """

        self.__category = None
        self.__conditions = []
        self.__action = []

        self.assign_values(rule_details)

    @property
    def category(self):
        return self.__category

    @category.setter
    @validator(VALIDATION['rule_category'])
    def category(self, category):
        self.__category = category

    @property
    def conditions(self):
        return self.__conditions

    @conditions.setter
    def conditions(self, conditions):
        if isinstance(conditions, dict):
            conditions = [conditions]
        temp = []
        for condition in conditions:
            if isinstance(condition, dict):
                temp.append(RuleConditionEntity(condition))
        
        self.__conditions = temp

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        if isinstance(action, dict):
            action = [action]
        temp = []
        for row in action:
            if isinstance(row, dict):
                temp.append(RuleActionEntity(row))

        self.__action = temp
