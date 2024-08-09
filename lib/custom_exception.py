
class DBException(Exception):
    '''
    @summary: if connection with database cant be established
    '''

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class DBConnectionError(DBException):

    def __init__(self, message):
        self.message = message


class DBQueryError(DBException):

    def __init__(self, message):
        self.message = message

class ValidationException(Exception):
    '''validation exception'''

    def __init__(self, msg=None):
        super(ValidationException, self).__init__(msg)
        self.msg = msg
