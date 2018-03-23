"""
.. module:: app_error
   :synopsis: Custom exception class so we can wrap other exceptions and
    format the output.
.. moduleauthor:: John Pappas <jstevenpappas at gmail.com>

"""


class AppError(Exception):
    """Generic exception for the application"""
    def __init__(self, msg, original_exception):
        super(AppError, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
