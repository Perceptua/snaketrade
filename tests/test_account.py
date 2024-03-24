from datetime import datetime, timedelta, timezone
from snaketrade.account import ETradeAccount
from snaketrade.auth import Auth
from snaketrade.snaketradeutils import SnakeTradeUtils as stu
import json
import pandas as pd
import unittest as ut
import webbrowser


class TestETradeAccount(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = 'prod'
        cls.date_fmt = '%m%d%Y'
        cls.test_accounts = cls.getTestAccounts()
        cls.auth = Auth(cls.env)
        cls.auth.set_auth_components()
        webbrowser.open(cls.auth.authorize_url)
        cls.verification_code = input('Enter verification code: ')
        cls.auth.make_session(cls.verification_code)

    @classmethod
    def getTestAccounts(cls):
        with open('tests/data/accounts.json') as f:
            test_accounts = json.load(f)['accounts']

        return test_accounts

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
        test_account = account_list[0]
        test_account_id = test_account['accountId']
        balance_response = account.get_account_balance(test_account)
        response_account_id = balance_response['accountId']
        self.assertIsInstance(balance_response, dict)

        if self.env == 'prod':
            self.assertEqual(test_account_id, response_account_id)

    def testGetAccountTransactions(self):
        account = ETradeAccount(self.auth)
        test_account = self.test_accounts['0']
        transactions, info = account.get_account_transactions(test_account)
        self.assertIsInstance(transactions, pd.DataFrame)

        if self.env == 'prod':
            start_date = datetime.now(tz=timezone.utc) - timedelta(days=100)
            end_date = datetime.now(tz=timezone.utc)
            count_transactions = 1
            sort_order = 'ASC'
            sort_order_bool = True if sort_order == 'ASC' else False

            transactions, info = account.get_account_transactions(
                test_account,
                start_date=start_date.strftime(self.date_fmt),
                end_date=end_date.strftime(self.date_fmt),
                sort_order=sort_order, count_transactions=count_transactions
            )

            transactions.transactionDate = transactions.transactionDate.apply(
                lambda x: stu.utc_from_milliseconds(x)
            )

            dates_sorted = transactions.transactionDate.sort_values(
                ascending=sort_order_bool
            )

            self.assertEqual(
                list(transactions.transactionDate), list(dates_sorted)
            )

            self.assertGreaterEqual(
                transactions.transactionDate.min(), start_date
            )

            self.assertLessEqual(transactions.transactionDate.max(), end_date)
            self.assertEqual(count_transactions, transactions.shape[0])

            transactions, info = account.get_account_transactions(
                test_account,
                marker=info.marker.values[0]
            )

            self.assertFalse('marker' in info.columns)
            self.assertEqual(count_transactions, transactions.shape[0])


if __name__ == '__main__':
    ut.main()
