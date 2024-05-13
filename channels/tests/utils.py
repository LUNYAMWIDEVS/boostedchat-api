from django.test import TestCase
from colorama import Fore, Style, init
import sys


class TestUtils(TestCase):
    def describe(self, message, level=0):
        tabs = '\t' * level
        print(Fore.BLUE + f"{tabs}{message}")

    def should(self, message, success = True, level=0, error_msg=""):
        print(self.shouldMessage(message, success, level))
        if not success:
            print(Style.RESET_ALL)
            raise AssertionError(error_msg)
            sys.exit()

    def shouldMessage(self, message, success = True, level=0):
        level +=1
        tabs = '\t' * level
        return (Fore.GREEN if success == True else Fore.RED) + f"{tabs}{'✓ ' if success == True else '✗ '}{message}"
    
    def localTest(self, test_func, *args, **kwargs):
        should = kwargs.pop('should', "")  # Extract 'should' from kwargs, default to "" if not present
        level = kwargs.pop('level', 0)    # Extract 'level' from kwargs, default to 0 if not present
        success = True
        error_msg = ""
        try:
            test_func(*args, **kwargs)
        except AssertionError as e:
            error_msg = str(e)
            success = False
        self.should(should, success, level, error_msg)


