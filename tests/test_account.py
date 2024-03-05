from datetime import datetime as dt, timedelta as td
from snaketrade.account import ETradeAccount
from snaketrade.auth import Auth
from xml.etree import ElementTree as et
import pandas as pd
import unittest as ut
import webbrowser


class TestETradeAccount(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = 'sandbox'
        cls.auth = Auth(cls.env)
        cls.auth.set_auth_components()
        webbrowser.open(cls.auth.authorize_url)
        cls.verification_code = input('Enter verification code: ')
        cls.auth.make_session(cls.verification_code)

    def testInit(self):
        account = ETradeAccount(self.auth)
        self.assertIsInstance(account.auth, Auth)

    def testGetAccountList(self):
        account = ETradeAccount(self.auth)
        account_list = account.get_account_list()
        self.assertIsInstance(account_list, list)
        self.assertIn('accountId', account_list[0].keys())

    def testGetAccountBalance(self):
        account = ETradeAccount(self.auth)
        account_list = account.get_account_list()
        first_account = account_list[0]
        balance_response = account.get_account_balance(first_account)
        self.assertIsInstance(balance_response, str)
        self.assertIn('xml version="1.0"', balance_response)
        first_account_type = first_account['accountType']

        balance_response = account.get_account_balance(
            first_account, account_type=first_account_type
        )

        self.assertIn(first_account_type, balance_response)
        fake_account_type = 'NONE'

        balance_response = account.get_account_balance(
            first_account, account_type=fake_account_type
        )

        self.assertNotIn(fake_account_type, balance_response)

    def testGetAccountTransactions(self):
        account = ETradeAccount(self.auth)
        account_list = account.get_account_list()
        first_account = account_list[0]
        transaction_list = account.get_account_transactions(first_account)
        self.assertIsInstance(transaction_list, str)
        self.assertIn('xml version="1.0"', transaction_list)


if __name__ == '__main__':
    ut.main()
