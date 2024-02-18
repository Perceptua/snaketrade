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
        
    def testGetConsumerKeyAndSecret(self):
        env = 'sandbox'
        auth = Auth(env)
        consumer_key, consumer_secret = auth.get_consumer_key_and_secret()
        self.assertIsInstance(consumer_key, str)
        self.assertIsInstance(consumer_secret, str)
        
        env = 'prod'
        auth = Auth(env)
        consumer_key, consumer_secret = auth.get_consumer_key_and_secret()
        self.assertIsInstance(consumer_key, str)
        self.assertIsInstance(consumer_secret, str)
        
        env = 'invalid'
        auth = Auth(env)
        self.assertRaises(KeyError, auth.get_consumer_key_and_secret)
        
    def testGetOauthService(self):
        env = 'sandbox'
        auth = Auth(env)
        base_url = auth.get_base_url()
        consumer_key, consumer_secret = auth.get_consumer_key_and_secret()
        
        oauth_service = auth.get_oauth_service(
            base_url, consumer_key, consumer_secret
        )
        
        self.assertIsInstance(oauth_service, OAuth1Service)
        
    def testGetRequestTokenAndSecret(self):
        env = 'sandbox'
        auth = Auth(env)
        base_url = auth.get_base_url()
        consumer_key, consumer_secret = auth.get_consumer_key_and_secret()
        
        oauth_service = auth.get_oauth_service(
            base_url, consumer_key, consumer_secret
        )
        
        request_token, request_secret = auth.get_request_token_and_secret(
            oauth_service
        )
        
        self.assertIsInstance(request_token, str)
        self.assertIsInstance(request_secret, str)
        
    def testGetAuthorizeURL(self):
        env = 'sandbox'
        auth = Auth(env)
        authorize_url = auth.get_authorize_url()
        self.assertIn('https://us.etrade.com/e/t/etws', authorize_url)
        

if __name__ == '__main__':
    ut.main()