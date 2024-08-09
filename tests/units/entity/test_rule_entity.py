import pytest
from lib.custom_exception import ValidationException
from src.entity.rule_entity import RuleConditionEntity, RuleActionEntity, RuleDetailEntity


class TestRuleConditionEntity:
    @pytest.mark.parametrize(
        "input, error",
        [
            ({"field": "from","operator": "contains","value": 'test@gmail.com'}, 0),
            ({"field": "received_date","operator": "less than","value": '1', "duration_type": "day"}, 0),
            ({"field": "from","operator": "less than","value": 'test@gmail.com'}, 1),
            ({"operator": "less than", "field": "from","value": 'test@gmail.com'}, 1),
            ({"field": "from","operator": "less than","value": 'test@gmail.com'}, 1),
            ({"field": "from","operator": "test","value": 'test@gmail.com'}, 1),
        ])
    def test_entity_validations(self, input, error):
        if error:
            with pytest.raises(ValidationException):
                RuleConditionEntity(input)
        else:
            output = RuleConditionEntity(input)
            for key,value in input.items():
                assert value == getattr(output, key)


class TestRuleActionEntity:
    @pytest.mark.parametrize(
        "input, error",
        [
            ({"category": "read"}, 0),
            ({"category": "unread"}, 0),
            ({"category": "move", "value": "inbox"}, 0),
            ({"category": "reads"}, 1),
        ])
    def test_entity_validations(self, input, error):
        if error:
            with pytest.raises(ValidationException):
                RuleActionEntity(input)
        else:
            output = RuleActionEntity(input)
            for key,value in input.items():
                assert value == getattr(output, key)


class TestRuleDetailEntity:
    @pytest.mark.parametrize(
        "input, error",
        [
            ({"category": "all", "conditions": [{"field": "from", "operator": "contains", "value": "test@gmail.com"}], "action": [{"type": "move", "value": "Inbox"}]}, 0),
            ({"category": "all", "conditions": {"field": "from", "operator": "contains", "value": "test@gmail.com"}, "action": {"type": "move", "value": "Inbox"}}, 0),
        ])
    def test_entity_validations(self, input, error):
        if error:
            with pytest.raises(ValidationException):
                RuleDetailEntity(input)
        else:
            output = RuleDetailEntity(input)
            for key,value in input.items():
                if isinstance(value, str):
                    assert value == getattr(output, key)
                else:
                    temp =value
                    if isinstance(value, dict):
                        temp = [value]
                    for index, row in enumerate(temp):
                        for key_b, value_b in row.items():
                            assert value_b == getattr(getattr(output, key)[index], key_b)