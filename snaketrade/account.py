"""
Classes for reading account data.

Use ETradeAccount to list E-Trade accounts, balances, transactions, &
portfolios.

"""
from snaketrade.snaketradeutils import SnakeTradeUtils as stu
import pandas as pd


class ETradeAccount:
    """Get E-Trade account list, balances, transactions, & portfolios."""

    def __init__(self, auth):
        """
        Create an ETradeAccount instance.

        Parameters
        ----------
        auth : snaketrade.auth.ETradeAuth
            Authenticated ETradeAuth instance.

        Returns
        -------
        None.

        """
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

    def get_balance(self, account):
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

    def get_transactions(
        self, account, count_transactions=None, start_date=None, end_date=None,
        sort_order=None, marker=None
    ):
        """
        Get transactions for specified account.

        The default behavior retrieves the 50 most recent transactions. Use
        optional parameters to specify advanced search criteria.

        Parameters
        ----------
        account : dict
            Dictionary of account information returned by get_account_list.
        count_transactions : int, optional
            If supplied, specifies number of transactions to be retrieved. If
            None, the API default of 50 transactions will be returned. The
            default is None.
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
        params = {}

        if count_transactions:
            params['count'] = count_transactions

        if start_date:
            params['startDate'] = start_date

        if end_date:
            params['endDate'] = end_date

        if sort_order:
            params['sortOrder'] = sort_order

        if marker:
            params['marker'] = marker

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
        transactions = [stu.dict_to_dataframe(t) for t in transactions]
        transactions = pd.concat(transactions, ignore_index=True)
        transaction_info = stu.dict_to_dataframe(transaction_list_response)

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

    def get_portfolios(
        self, account, count_positions=None, sort_by=None, sort_order=None,
        page_number=None, market_session=None, view=None,
        totals_required=False, lots_required=False
    ):
        """
        Get portfolios for specified account.

        The default behavior retrieves the 50 most recent positions for each
        portfolio. Use optional parameters to specify advanced search criteria.

        Parameters
        ----------
        account : dict
            Dictionary of account information returned by get_account_list.
        count_positions : int, optional
            If supplied, specifies the number of positions to be retrieved. The
            default is None.
        sort_by : str, optional
            Optional key to use for sorting positions. For allowed values, see
            https://apisb.etrade.com/docs/api/account/api-portfolio-v1.html.
            The default is None.
        sort_order : str, optional
            Optional sort order for retrieved positions. Must be either 'ASC'
            (ascending) or 'DSC' (descending). The default is None.
        page_number : int, optional
            If supplied, the specified page of positions within the portfolio
            will be requested. The default is None.
        market_session : str, optional
            Optional parameter to include extended-hours positions. For allowed
            values, see
            https://apisb.etrade.com/docs/api/account/api-portfolio-v1.html.
            The default is None.
        view : str, optional
            Optional view parameter to retrieve position data. For allowed
            values, see
            https://apisb.etrade.com/docs/api/account/api-portfolio-v1.html.
            The default is None.
        totals_required : bool, optional
            If True, include portfolio totals in response. The default is
            False.
        lots_required : bool, optional
            If True, return portfolio lots in response. The default is False.

        Returns
        -------
        portfolios : list
            List of tuples of the form (positions, info), where both positions
            & info are dataframes. Positions contains one record for each
            portfolio position, while info is a single-record dataframe of
            portfolio metadata.

        """
        params = {}

        if count_positions:
            params['count'] = count_positions

        if sort_by:
            params['sortBy'] = sort_by

        if sort_order:
            params['sortOrder'] = sort_order

        if page_number:
            params['pageNumber'] = page_number

        if market_session:
            params['marketSession'] = market_session

        if view:
            params['view'] = view

        if totals_required:
            params['totalsRequired'] = True

        if lots_required:
            params['lotsRequired'] = True

        account_id_key = account['accountIdKey']
        url = f'{self.auth.base_url}/v1/accounts/{account_id_key}/portfolio'

        response = self.auth.session.get(
            url,
            header_auth=True,
            headers=self.headers,
            params=params
        )

        data = stu.parse_response_json(response)
        portfolio_response = data['PortfolioResponse']['AccountPortfolio']
        portfolios = []

        for portfolio in portfolio_response:
            positions = portfolio.pop('Position')
            positions = [stu.dict_to_dataframe(p) for p in positions]
            positions = pd.concat(positions, ignore_index=True)
            portfolio_info = stu.dict_to_dataframe(portfolio)
            portfolios += [(positions, portfolio_info)]

        return portfolios
