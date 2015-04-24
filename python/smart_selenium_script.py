__author__ = 'aivaneyko'
import sys
from selenium import webdriver

class smartSeleniumScript(object):


        def __init__(self, *args, **kwargs):
            """
            Define flow of state runs, each state is are dict which consists of next str, previous str, exceptions_map keys dict.
            exceptions_map dict is are dict which consists of reason (key) and action_to_resolve (value)
            """
            self.flow = {
                'init':{
                    'next': 'authenticate'
                },
                'authenticate': {
                    'previous': 'authenticate',
                    'next': 'first_action',
                    'exceptions_map': {'reason': 'action_to_resolve'}
                },
                'first_action': {
                    'previous': 'authenticate',
                    'next': 'second_action',
                    'exceptions_map': {'reason': 'action_to_resolve'}
                },
                'second_action': {
                    'previous': 'first_action',
                    'next': 'third_action',
                    'exceptions_map': {'reason': 'action_to_resolve'}
                },
                'third_action': {
                    'previous': 'second_action',
                    'next': 'finish',
                    'exceptions_map': {'reason': 'action_to_resolve'}
                },
            }
            self.state = self.set_state('init')

        def authenticate(self, driver, login, password, url, *args, **kwargs):
            """
            Perform authentication actions
            :param driver:
            :param login:
            :param password:
            :param url:
            :return:
            """
            driver.get(url)
            self.set_state('authenticate')
            try:
                # perform authentication action with login['selector'], login['value']), password['selector'], password['value']
                pass
            except:
                reason = self.find_reason(sys.exc_info()[0])
                state = self.get_state()
                # Try to handle error
                self.handle_error(state, reason)
            self.set_state('first_action')

        def first_action(self, driver, search_field, states, *args, **kwargs):
            """
            perform logic for adding product
            :param driver:
            :param search_field:
            :param states:
            :return:
            """
            try:
                #
                pass
            except:
                reason = self.find_reason(sys.exc_info()[0])
                next_state = self.exceptions_map[reason]
                self.set_state('authenticate')
                self.handle_error()

        def second_action(self, driver, *args, **kwargs):
            """
            Access checkout page
            :param driver:
            :return:
            """
            pass

        def third_action(self, driver, *args, **kwargs):
            """
            Apply coupon
            :param driver:
            :return:
            """
            pass

        def handle_error(self, state, reason):
            error_resolver = self.flow[state]['exceptions_map'][reason]
            self.set_state(error_resolver)
            return self.next_step()

        def next_step(self):
            self.next = getattr(self, self.get_state())
            return next()

        def set_state(self, state):
            self.state = state

        def get_state(self, state):
            return self.state

        def find_reason(self, error):
            # return reason of error, reason identified by raised error, self.state;also we may log and analyse states
            # to define reason
            pass

        def action_to_resolve(self):
            """
            Apply logic to resolve error, set_state to valid value.
            :return:
            """
            pass

# Usage example
class seleniumScript(smartSeleniumScript):

    def run(self):
        # Define params for authentication
	driver = webdriver.Firefox()
        login = {'selector':'#login', 'value': '88eugenie@gmail.com'}
        password = {'selector':'#password', 'value': '88driver'}
        url = 'www.somesite.com/Login'
        self.authenticate(driver, login, password, url)
        # Define arguments required for base_driver.first_action
        self.first_action(driver)
        self.second_action(driver)
        self.third_action(driver)
