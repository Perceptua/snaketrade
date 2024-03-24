from snaketrade.auth import ETradeAuth
from rauth import OAuth1Service, OAuth1Session
import unittest as ut
import webbrowser


class TestAuth(ut.TestCase):
    def testInit(self):
        env = 'sandbox'
        auth = ETradeAuth(env)
        self.assertIsInstance(auth, ETradeAuth)
        self.assertEqual(auth.env, env)

        env = 'prod'
        auth = ETradeAuth(env)
        self.assertIsInstance(auth, ETradeAuth)
        self.assertEqual(auth.env, env)

        env = 'invalid'
        self.assertRaises(KeyError, ETradeAuth, env)

    def testGetConsumerKey(self):
        env = 'sandbox'
        auth = ETradeAuth(env)
        consumer_key, consumer_secret = auth.get_consumer_key()
        self.assertIsInstance(consumer_key, str)
        self.assertIsInstance(consumer_secret, str)

        env = 'prod'
        auth = ETradeAuth(env)
        consumer_key, consumer_secret = auth.get_consumer_key()
        self.assertIsInstance(consumer_key, str)
        self.assertIsInstance(consumer_secret, str)

    def testGetOauthService(self):
        env = 'sandbox'
        auth = ETradeAuth(env)
        consumer_key, consumer_secret = auth.get_consumer_key()

        oauth_service = auth.get_oauth_service(
            auth.base_url, consumer_key, consumer_secret
        )

        self.assertIsInstance(oauth_service, OAuth1Service)

    def testGetRequestToken(self):
        env = 'sandbox'
        auth = ETradeAuth(env)
        consumer_key, consumer_secret = auth.get_consumer_key()

        oauth_service = auth.get_oauth_service(
            auth.base_url, consumer_key, consumer_secret
        )

        request_token, request_token_secret = auth.get_request_token(
            oauth_service
        )

        self.assertIsInstance(request_token, str)
        self.assertIsInstance(request_token_secret, str)

    def testFormatAuthorizeURL(self):
        env = 'sandbox'
        auth = ETradeAuth(env)
        consumer_key, consumer_secret = auth.get_consumer_key()

        oauth_service = auth.get_oauth_service(
            auth.base_url, consumer_key, consumer_secret
        )

        request_token, _ = auth.get_request_token(
            oauth_service
        )

        authorize_url = auth.format_authorize_url(oauth_service, request_token)
        self.assertIn('https://us.etrade.com/e/t/etws', authorize_url)

    def testSetAuthComponents(self):
        env = 'sandbox'
        auth = ETradeAuth(env)
        auth.set_auth_components()
        self.assertIn('apisb.etrade.com', auth.base_url)
        self.assertIsInstance(auth.oauth_service, OAuth1Service)
        self.assertIsInstance(auth.request_token, str)
        self.assertIsInstance(auth.request_token_secret, str)
        self.assertIn('https://us.etrade.com/e/t/etws', auth.authorize_url)

    def testMakeSession(self):
        env = 'sandbox'
        auth = ETradeAuth(env)
        auth.set_auth_components()
        webbrowser.open(auth.authorize_url)
        verification_code = input('Enter verification code: ')
        auth.make_session(verification_code)
        self.assertIsInstance(auth.session, OAuth1Session)
