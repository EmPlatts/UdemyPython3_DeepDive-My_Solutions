"""PROJECT 5: Enumeration
An easy way to generate exceptions.
Functionality:
    - single enumeration AppException
    - exceptions have a name (key) and three associated values:
        - name (e.g. NotAnInteger)
        - code (e.g. 100)
        - default message (e.g. 'Value is not an integer.')
        - associated exception type (e.g. ValueError)
    - lookup by exception name (key) or code (value)
        AppException['NotAnInteger']    AppException(100)
    - method to raise an exception
        AppException.Timeout.throw()
    - ability to override default message when throwing exception
        AppException.Timeout.throw('Timeout connecting to DB.')
Tips:
    - enumeration members will be defined using a tuple containing:
        - code, exception type, default message
    - Use the __new__ approach
    - Make the value the error code
    - Provide an additional proprty for message
"""
import enum

@enum.unique
class AppException(enum.Enum):
    General = 100, Exception, 'Application error'
    Timeout = 101, TimeoutError, 'Application call has timed out'
    NotAnInteger = 102, ValueError, 'Value must be an integer'
    NotAList = 103, ValueError, 'Value must be a list'

    def __new__(cls, exception_code, exception_class, exception_message):
        member = object.__new__(cls)

        member._value_ = exception_code
        member.exception = exception_class
        member.message = exception_message
        
        return member
    
    @property
    def code(self):
        return self.value

    def throw(self, message=None):
        message = message or self.message
        raise self.exception(f'{self.code} : {self.message}')

print([(ex.name, ex.code, ex.message) for ex in AppException])
