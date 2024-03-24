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

    def testGetBalance(self):
        account = ETradeAccount(self.auth)
        account_list = account.get_account_list()
        test_account = account_list[0]
        test_account_id = test_account['accountId']
        balance_response = account.get_balance(test_account)
        response_account_id = balance_response['accountId']
        self.assertIsInstance(balance_response, dict)

        if self.env == 'prod':
            self.assertEqual(test_account_id, response_account_id)

    def testGetTransactions(self):
        account = ETradeAccount(self.auth)
        account_list = account.get_account_list()
        test_account = account_list[0]
        transactions, info = account.get_transactions(test_account)
        self.assertIsInstance(transactions, pd.DataFrame)
        self.assertGreaterEqual(transactions.shape[0], 1)
        self.assertIsInstance(info, pd.DataFrame)
        self.assertEqual(info.shape[0], 1)

        if self.env == 'prod':
            test_account = self.test_accounts['0']
            count_transactions = 1
            start_date = datetime.now(tz=timezone.utc) - timedelta(days=100)
            end_date = datetime.now(tz=timezone.utc)
            sort_order = 'ASC'
            sort_order_bool = True if sort_order == 'ASC' else False

            transactions, info = account.get_transactions(
                test_account,
                count_transactions=count_transactions,
                start_date=start_date.strftime(self.date_fmt),
                end_date=end_date.strftime(self.date_fmt),
                sort_order=sort_order
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

            transactions, info = account.get_transactions(
                test_account,
                marker=info.marker.values[0]
            )

            self.assertFalse('marker' in info.columns)
            self.assertEqual(count_transactions, transactions.shape[0])

    def testGetTransactionDetails(self):
        account = ETradeAccount(self.auth)
        account_list = account.get_account_list()
        test_account = account_list[0]
        transactions, _ = account.get_transactions(test_account)
        transaction_id = transactions.loc[0, 'transactionId']

        transaction_details = account.get_transaction_details(
            test_account, transaction_id
        )

        self.assertIsInstance(transaction_details, pd.DataFrame)
        self.assertEqual(transaction_details.shape[0], 1)
        self.assertIn('transactionId', list(transaction_details.columns))

        if self.env == 'prod':
            test_account = self.test_accounts['0']
            transactions, _ = account.get_transactions(test_account)
            transaction_id = transactions.loc[0, 'transactionId']
            expected_amount = transactions.loc[0, 'amount']

            transaction_details = account.get_transaction_details(
                test_account, transaction_id
            )

            self.assertEqual(
                transaction_details.loc[0, 'amount'], expected_amount
            )

    def testGetPortfolio(self):
        account = ETradeAccount(self.auth)

        # 2024-03-24: View Portfolio endpoint only working in production
        if self.env == 'prod':
            test_account = self.test_accounts['0']
            count_positions = 2
            sort_by = 'SYMBOL'
            sort_order = 'ASC'
            page_number = 1
            market_session = 'EXTENDED'
            view = 'COMPLETE'
            totals_required = True
            lots_required = True

            portfolios = account.get_portfolios(
                test_account,
                count_positions=count_positions,
                sort_by=sort_by,
                sort_order=sort_order,
                page_number=page_number,
                market_session=market_session,
                view=view,
                totals_required=totals_required,
                lots_required=lots_required
            )

            for positions, info in portfolios:
                self.assertIsInstance(positions, pd.DataFrame)
                self.assertIsInstance(info, pd.DataFrame)
                self.assertEqual(positions.shape[0], count_positions)
                self.assertEqual(info.shape[0], 1)
                symbols_sorted = list(sorted(positions.symbol))
                self.assertEqual(list(positions.symbol), symbols_sorted)
