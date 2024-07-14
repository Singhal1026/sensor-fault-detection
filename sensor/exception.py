import sys
import os


def error_message_details(error, error_detail:sys):

    _,_,exc_tb = error_detail.exc_info()
    filename = exc_tb.tb_frame.f_code.co_filename

    error_message = f"Error occured in File [{filename}] in line no. [{exc_tb.tb_lineno}] with error message [{error}]"
    return error_message


class SensorException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)

        self.error_message = error_message_details(error_message, error_details)

    def __str__(self):
        return self.error_message