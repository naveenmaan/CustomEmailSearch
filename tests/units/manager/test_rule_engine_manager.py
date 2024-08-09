import json

import pytest
import builtins

from lib.custom_exception import ValidationException

from src.entity.rule_entity import RuleDetailEntity
from src.manager.rule_engine_manager import RuleEngineManager


class TestRuleEngineManager:

    @pytest.mark.parametrize(
        "input, expected_output, error_type",
        [
            ({"rule_name": {"category": "all",
                            "conditions": [{"field": "from", "operator": "contains", "value": "test@gmail.com"}],
                            "action": [{"type": "move", "value": "Inbox"}]}},
             {"rule_name": {"category": "all",
                            "conditions": [{"field": "from", "operator": "contains", "value": "test@gmail.com"}],
                            "action": [{"type": "move", "value": "Inbox"}]}}, None),
            ({"rule_name": {"category": "all",
                            "conditions": [{"field": "received_date", "operator": "contains", "value": "test@gmail.com"}],
                            "action": [{"type": "move", "value": "Inbox"}]}}, {}, ValidationException)

        ]
    )
    def test_get_rules_list(self, monkeypatch, input, expected_output, error_type):
        """method to test the get rules list method"""

        def mock_open(filename, mode):
            return MockFile(json.dumps(input))

        class MockFile:
            def __init__(self, content):
                self.content = content

            def read(self):
                return self.content

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        monkeypatch.setattr("builtins.open", mock_open)

        if error_type:
            with pytest.raises(error_type):
                rule_engine_obj = RuleEngineManager()
        else:
            rule_engine_obj = RuleEngineManager()
            for key_A, value_A in expected_output.items():
                input = value_A
                output = rule_engine_obj.get_rule_by_name(key_A)
                for key, value in input.items():
                    if isinstance(value, str):
                        assert value == getattr(output, key)
                    else:
                        temp = value
                        if isinstance(value, dict):
                            temp = [value]
                        for index, row in enumerate(temp):
                            for key_b, value_b in row.items():
                                assert value_b == getattr(getattr(output, key)[index], key_b)

    def test_get_rules_list_file_not_found(self, monkeypatch):
        """method to test the get rules list method"""

        def mock_open(filename, mode):
            raise FileNotFoundError("not found")

        monkeypatch.setattr("builtins.open", mock_open)

        with pytest.raises(FileNotFoundError):
            RuleEngineManager()

    @pytest.mark.parametrize(
        "input, expected_output",
        [
            ({"rule_name": {"category": "all",
                            "conditions": [{"field": "from", "operator": "contains", "value": "test@gmail.com"}],
                            "action": [{"type": "move", "value": "Inbox"}]}}, "from_address rlike 'test@gmail.com'"),
            ({"rule_name": {"category": "all",
                            "conditions": [{"field": "from", "operator": "contains", "value": "test@gmail.com"},
                                           {"field": "received_date", "operator": "less than", "value": "2", "duration_type": "day"}],
                            "action": [{"type": "move", "value": "Inbox"}]}}, "from_address rlike 'test@gmail.com' and received_date < curdate() - interval 2 day"),
            ({"rule_name": {"category": "any",
                            "conditions": [{"field": "from", "operator": "contains", "value": "test@gmail.com"},
                                           {"field": "received_date", "operator": "less than", "value": "2",
                                            "duration_type": "day"}],
                            "action": [{"type": "move", "value": "Inbox"}]}},
             "from_address rlike 'test@gmail.com' or received_date < curdate() - interval 2 day")

        ]
    )
    def test_email_query_build_by_rule(self, monkeypatch, input, expected_output):
        def mock_open(filename, mode):
            return MockFile(json.dumps(input))

        class MockFile:
            def __init__(self, content):
                self.content = content

            def read(self):
                return self.content

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

        monkeypatch.setattr("builtins.open", mock_open)

        rule_engine_obj = RuleEngineManager()
        rule_detail_entity_obj = rule_engine_obj.get_rule_by_name("rule_name")
        assert rule_engine_obj.email_query_build_by_rule(rule_detail_entity_obj) == expected_output