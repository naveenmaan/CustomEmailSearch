import validictory
from lib.custom_exception import ValidationException


class validator():
    '''A decorator that validates the entities when used along with
        setter method of the entities
        :calling: @validator(schema)
        :schema: {"type":"integer","required":True,"minimum":1,}'''

    def __init__(self , schema):
        self.schema = schema

    def __call__(self , funct):
        def inner(*arg , **kwargs):
            try:
                validictory.validate(arg[1] , self.schema)
                funct(*arg , **kwargs)
            except Exception:
                raise ValidationException('InvalidData: %s does not have '
                                          'a valid data' % funct.__name__)

        return inner