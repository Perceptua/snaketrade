"""
Classes for reading account data.

Use ETradeAccount to list E-Trade accounts, balances, portfolios, &
transactions.
"""
from snaketrade.snaketradeutils import SnakeTradeUtils as stu
import json


class ETradeAccount:
    """
    Get E-Trade account list, balances, portfolios, & transactions.

    Requires auhorized session (can be created with snaketrade.auth.Auth).
    """

    def __init__(self, auth):
        self.auth = auth

    def get_account_list(self):
        """
        Retrieve account list from E-Trade.

        Returns
        -------
        account_list : list
            List of E-Trade accounts associated with the user. Each item is a
            dictionary of account information.

        """
        url = f'{self.auth.base_url}/v1/accounts/list.json'
        response = self.auth.session.get(url, header_auth=True)

        if response is not None and response.status_code == 200:
            data = json.loads(response.text)['AccountListResponse']
            account_list = data['Accounts']['Account']
        else:
            account_list = []

        return account_list

    def get_account_balance(self, account, account_type=None):
        """
        Get balance information for specified account.

        Parameters
        ----------
        account : dict
            Dictionary of account information returned by get_account_list.
        account_type : str, optional
            Optional account type parameter to send with balance request.
            Allowable values are detailed at
            https://apisb.etrade.com/docs/api/account/api-balance-v1.html

        Returns
        -------
        balance_response : str
            XML-formatted string of account balance information.

        """
        institution_type = account['institutionType']
        params = dict(instType=institution_type, realTimeNAV='true')

        if account_type:
            params['accountType'] = account_type

        account_id_key = account['accountIdKey']
        url = f'{self.auth.base_url}/v1/accounts/{account_id_key}/balance'
        response = self.auth.session.get(url, header_auth=True, params=params)

        if response is not None and response.status_code == 200:
            balance_response = response.text
        else:
            balance_response = ''.join([
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<BalanceResponse></BalanceResponse>'
            ])

        return balance_response

    def get_account_transactions(
        self, account, start_date=None, end_date=None, sort_order=None,
        marker=None, count_transactions=None
    ):
        date_format = '%m%d%Y'
        params = {}

        if start_date:
            stu.check_date_format(start_date, date_format)
            params['startDate'] = start_date

        if end_date:
            stu.check_date_format(end_date, date_format)
            params['endDate'] = end_date

        if sort_order:
            allowed_values = ['ASC', 'DESC']
            assert sort_order in allowed_values
            params['sortOrder'] = sort_order

        if marker:
            params['marker'] = marker

        if count_transactions:
            params['count'] = count_transactions

        account_id_key = account['accountIdKey']
        url = f'{self.auth.base_url}/v1/accounts/{account_id_key}/transactions'
        response = self.auth.session.get(url, header_auth=True, params=params)

        if response is not None and response.status_code == 200:
            transaction_list_response = response.text
        else:
            transaction_list_response = ''.join([
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<TransactionListResponse></TransactionListResponse>'
            ])

        return transaction_list_response
