"""
Classes for reading account data.

Use ETradeAccount to list E-Trade accounts, balances, portfolios, &
transactions.
"""
from snaketrade.snaketradeutils import SnakeTradeUtils as stu
import pandas as pd


class ETradeAccount:
    """
    Get E-Trade account list, balances, portfolios, & transactions.

    Requires auhorized session (can be created with snaketrade.auth.Auth).
    """

    def __init__(self, auth):
        self.auth = auth
        self.headers = {'Accept': 'application/json'}

    def get_account_list(self):
        """
        Retrieve account list from E-Trade.

        Returns
        -------
        account_list : list
            List of E-Trade accounts associated with the user. Each item is a
            dictionary of account information.

        """
        url = f'{self.auth.base_url}/v1/accounts/list'

        response = self.auth.session.get(
            url,
            header_auth=True,
            headers=self.headers
        )

        data = stu.parse_response_json(response)
        account_list = data['AccountListResponse']['Accounts']['Account']

        return account_list

    def get_account_balance(self, account):
        """
        Get balance information for specified account.

        Parameters
        ----------
        account : dict
            Dictionary of account information returned by get_account_list.

        Returns
        -------
        balance_response : dict
            Dictionary of account balance information.

        """
        institution_type = account['institutionType']
        params = dict(instType=institution_type, realTimeNAV='true')
        account_id_key = account['accountIdKey']
        url = f'{self.auth.base_url}/v1/accounts/{account_id_key}/balance'

        response = self.auth.session.get(
            url,
            header_auth=True,
            headers=self.headers,
            params=params
        )

        data = stu.parse_response_json(response)
        balance_response = data['BalanceResponse']

        return balance_response

    def get_account_transactions(
        self, account, start_date=None, end_date=None, sort_order=None,
        marker=None, count_transactions=None
    ):
        """
        Get transactions for specified account.

        The default behavior retrieves the 50 most recent transactions. Use
        optional parameters to specify advanced search criteria.

        Parameters
        ----------
        account : dict
            Dictionary of account information returned by get_account_list.
        start_date : str, optional
            Optional start date in mmddYYYY format. Transaction history is
            available for two years. The default is None.
        end_date : str, optional
            Optional end date in mmddYYYY format. Transaction history is
            available for two years. The default is None.
        sort_order : str, optional
            Optional date order of transactions returned. Must be either 'ASC'
            (ascending) or 'DSC' (descending). The default is None.
        marker : str, optional
            If supplied, specifies marker to retrieve page of transactions. If
            None, the first page matching other search criteria will be
            returned. The default is None.
        count_transactions : int, optional
            If supplied, specifies number of transactions to be retrieved. If
            None, the API default of 50 transactions will be returned. The
            default is None.

        Returns
        -------
        transactions : pandas.DataFrame
            Dataframe of account transactions. Dataframe includes one row per
            transaction.
        transaction_info : pandas.DataFrame
            Dataframe of transaction response metadata. If more transactions
            are available, the URI at transaction_info.next.values[0] can be
            used to retrieve the next page of transactions.

        """
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

        response = self.auth.session.get(
            url,
            header_auth=True,
            headers=self.headers,
            params=params
        )

        data = stu.parse_response_json(response)
        transaction_list_response = data['TransactionListResponse']
        transactions = transaction_list_response.pop('Transaction')
        transaction_info = stu.dict_to_dataframe(transaction_list_response)

        transactions = pd.concat([
            stu.dict_to_dataframe(t) for t in transactions
        ], ignore_index=True)

        return transactions, transaction_info

    def get_transaction_details(self, account, transaction_id):
        """
        Get details for specified transaction.

        Parameters
        ----------
        account : dict
            Dictionary of account information returned by get_account_list.
        transaction_id : str
            ID of transaction to be retrieved.

        Returns
        -------
        transaction : pandas.DataFrame
            Single-row dataframe of transaction details.

        """
        account_id_key = account['accountIdKey']

        url = '/'.join([
            self.auth.base_url, 'v1', 'accounts', account_id_key,
            'transactions', transaction_id
        ])

        response = self.auth.session.get(
            url,
            header_auth=True,
            headers=self.headers
        )

        data = stu.parse_response_json(response)
        transaction = stu.dict_to_dataframe(data['TransactionDetailsResponse'])

        return transaction
