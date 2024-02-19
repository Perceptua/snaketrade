# -*- coding: utf-8 -*-
from rauth import OAuth1Service
import os

class Auth:
    def __init__(self, env):
        self.env = env
        self.base_url = None
        self.oauth_service = None
        self.request_token = None
        self.request_token_secret = None
        self.authorize_url = None
        self.session = None
        
        self.env_map = {
            'sandbox': 'https://apisb.etrade.com',
            'prod': 'https://api.etrade.com'
        }
        
    def set_auth_components(self):
        self.base_url = self.get_base_url()
        consumer_key, consumer_secret = self.get_consumer_key()
        
        self.oauth_service = self.get_oauth_service(
            self.base_url, 
            consumer_key, 
            consumer_secret
        )
        
        self.request_token, self.request_token_secret = self.get_request_token(
            self.oauth_service
        )
        
        self.authorize_url = self.get_authorize_url(
            self.oauth_service, 
            self.request_token
        )
        
    def make_session(self, verification_code):
        self.session = self.oauth_service.get_auth_session(
            self.request_token,
            self.request_token_secret,
            params=dict(oauth_verifier=verification_code),
        )
                                
    def get_base_url(self):
        base_url = self.env_map[self.env]
            
        return base_url
    
    def get_consumer_key(self):
        env_str = f'ETRADE_{self.env.upper()}'
        consumer_key = os.environ[f'{env_str}_KEY']
        consumer_secret = os.environ[f'{env_str}_SECRET']
        
        return consumer_key, consumer_secret
    
    def get_oauth_service(self, base_url, consumer_key, consumer_secret):
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
        request_token, request_token_secret = oauth_service.get_request_token(
            params=dict(oauth_callback='oob', format='json')
        )
        
        return request_token, request_token_secret
    
    def get_authorize_url(self, oauth_service, request_token):
        authorize_url = oauth_service.authorize_url.format(
            consumer_key=oauth_service.consumer_key,
            request_token=request_token
        )
        
        return authorize_url
    