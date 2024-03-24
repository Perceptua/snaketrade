"""
Classes for API authorization.

Use ETradeAuth to create authorized sessions to the E-Trade API.
"""
from rauth import OAuth1Service
import os


class ETradeAuth:
    """Create authorized sessions to the E-Trade API."""

    def __init__(self, env):
        """
        Create an ETradeAuth instance.

        Parameters
        ----------
        env : str
            API environment used for authorization. Must be either 'sandbox' or
            'prod'.

        Returns
        -------
        None.

        """
        self.url_map = {
            'sandbox': 'https://apisb.etrade.com',
            'prod': 'https://api.etrade.com'
        }

        self.env = env
        self.base_url = self.url_map[self.env]
        self.oauth_service = None
        self.request_token = None
        self.request_token_secret = None
        self.authorize_url = None
        self.session = None

    def set_auth_components(self):
        """
        Set session authorization components.

        Returns
        -------
        None.

        """
        consumer_key, consumer_secret = self.get_consumer_key()

        self.oauth_service = self.get_oauth_service(
            self.base_url,
            consumer_key,
            consumer_secret
        )

        self.request_token, self.request_token_secret = self.get_request_token(
            self.oauth_service
        )

        self.authorize_url = self.format_authorize_url(
            self.oauth_service,
            self.request_token
        )

    def make_session(self, verification_code):
        """
        Create an authorized session.

        Parameters
        ----------
        verification_code : str
            Verification code obtained from in-app authorization flow.

        Returns
        -------
        None.

        """
        self.session = self.oauth_service.get_auth_session(
            self.request_token,
            self.request_token_secret,
            params=dict(oauth_verifier=verification_code),
        )

    def get_consumer_key(self):
        """
        Retrieve API consumer key & secret from local environment variables.

        Returns
        -------
        consumer_key : str
            API consumer key to use for authorization.
        consumer_secret : str
            API consumer secret to use for authorization.

        """
        env_str = f'ETRADE_{self.env.upper()}'
        consumer_key = os.environ[f'{env_str}_KEY']
        consumer_secret = os.environ[f'{env_str}_SECRET']

        return consumer_key, consumer_secret

    def get_oauth_service(self, base_url, consumer_key, consumer_secret):
        """
        Create an OAuth1Service instance for the E-Trade API.

        Parameters
        ----------
        base_url : str
            API base url.
        consumer_key : str
            API consumer key returned by get_consumer_key.
        consumer_secret : str
            API consumer secret returned by get_consumer_key.

        Returns
        -------
        oauth_service : rauth.OAuth1Service
            OAuth 1.0 service used to get request tokens & create authorized
            sessions.

        """
        params = 'key={consumer_key}&token={request_token}'

        oauth_service = OAuth1Service(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            name='etrade',
            request_token_url=f'{base_url}/oauth/request_token',
            access_token_url=f'{base_url}/oauth/access_token',
            authorize_url=f'https://us.etrade.com/e/t/etws/authorize?{params}',
            base_url=base_url
        )

        return oauth_service

    def get_request_token(self, oauth_service):
        """
        Get API request token.

        Parameters
        ----------
        oauth_service : rauth.OAuth1Service
            OAuth 1.0 service used to get request tokens & create authorized
            sessions.

        Returns
        -------
        request_token : str
            Request token for the E-Trade API.
        request_token_secret : str
            Request token secret for the E-Trade API.

        """
        request_token, request_token_secret = oauth_service.get_request_token(
            params=dict(oauth_callback='oob', format='json')
        )

        return request_token, request_token_secret

    def format_authorize_url(self, oauth_service, request_token):
        """
        Format the authorization URL of the specified OAuth service.

        Parameters
        ----------
        oauth_service : rauth.OAuth1Service
            OAuth 1.0 service used to get request tokens & create authorized
            sessions.
        request_token : str
            Request token returned by get_request_token.

        Returns
        -------
        authorize_url : str
            Formatted authorization URL.

        """
        authorize_url = oauth_service.authorize_url.format(
            consumer_key=oauth_service.consumer_key,
            request_token=request_token
        )

        return authorize_url
