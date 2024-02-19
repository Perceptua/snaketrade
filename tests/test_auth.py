# -*- coding: utf-8 -*-
from snaketrade.auth import Auth
from rauth import OAuth1Service
import unittest as ut


class TestAuth(ut.TestCase):
    def testInit(self):
        env = 'sandbox'
        auth = Auth(env)
        self.assertIsInstance(auth, Auth)
        self.assertEqual(auth.env, env)
        
        env = 'prod'
        auth = Auth(env)
        self.assertIsInstance(auth, Auth)
        self.assertEqual(auth.env, env)
        
        env = 'invalid'
        auth = Auth(env)
        self.assertIsInstance(auth, Auth)
        self.assertEqual(auth.env, env)
        
    def testGetBaseURL(self):
        env = 'sandbox'
        auth = Auth(env)
        base_url = auth.get_base_url()
        self.assertIn('apisb.etrade.com', base_url)
        
        env = 'prod'
        auth = Auth(env)
        base_url = auth.get_base_url()
        self.assertIn('api.etrade.com', base_url)
        
        env = 'invalid'
        auth = Auth(env)
        self.assertRaises(KeyError, auth.get_base_url)
        
    def testGetConsumerKey(self):
        env = 'sandbox'
        auth = Auth(env)
        consumer_key, consumer_secret = auth.get_consumer_key()
        self.assertIsInstance(consumer_key, str)
        self.assertIsInstance(consumer_secret, str)
        
        env = 'prod'
        auth = Auth(env)
        consumer_key, consumer_secret = auth.get_consumer_key()
        self.assertIsInstance(consumer_key, str)
        self.assertIsInstance(consumer_secret, str)
        
        env = 'invalid'
        auth = Auth(env)
        self.assertRaises(KeyError, auth.get_consumer_key)
        
    def testGetOauthService(self):
        env = 'sandbox'
        auth = Auth(env)
        base_url = auth.get_base_url()
        consumer_key, consumer_secret = auth.get_consumer_key()
        
        oauth_service = auth.get_oauth_service(
            base_url, consumer_key, consumer_secret
        )
        
        self.assertIsInstance(oauth_service, OAuth1Service)
        
    def testGetRequestToken(self):
        env = 'sandbox'
        auth = Auth(env)
        base_url = auth.get_base_url()
        consumer_key, consumer_secret = auth.get_consumer_key()
        
        oauth_service = auth.get_oauth_service(
            base_url, consumer_key, consumer_secret
        )
        
        request_token, request_token_secret = auth.get_request_token(
            oauth_service
        )
        
        self.assertIsInstance(request_token, str)
        self.assertIsInstance(request_token_secret, str)
        
    def testGetAuthorizeURL(self):
        env = 'sandbox'
        auth = Auth(env)
        base_url = auth.get_base_url()
        consumer_key, consumer_secret = auth.get_consumer_key()
        
        oauth_service = auth.get_oauth_service(
            base_url, consumer_key, consumer_secret
        )
        
        request_token, _ = auth.get_request_token(
            oauth_service
        )
        
        authorize_url = auth.get_authorize_url(oauth_service, request_token)
        self.assertIn('https://us.etrade.com/e/t/etws', authorize_url)
        
    def testSetAuthComponents(self):
        env = 'sandbox'
        auth = Auth(env)
        auth.set_auth_components()
        self.assertIn('apisb.etrade.com', auth.base_url)
        self.assertIsInstance(auth.oauth_service, OAuth1Service)
        self.assertIsInstance(auth.request_token, str)
        self.assertIsInstance(auth.request_token_secret, str)
        self.assertIn('https://us.etrade.com/e/t/etws', auth.authorize_url)
        

if __name__ == '__main__':
    ut.main()