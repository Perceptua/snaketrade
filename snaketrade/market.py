"""
Classes for retrieving market data.

Use ETradeMarket to retrieve market data via the E-Trade API.

"""


class ETradeMarket:
    """Retrieve market data via the E-Trade API."""

    def __init__(self, auth):
        """
        Create an ETradeMarket instance.

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
