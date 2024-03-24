from snaketrade.auth import ETradeAuth
from snaketrade.market import ETradeMarket
import unittest as ut
import webbrowser


class TestETradeAccount(ut.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = 'prod'
        cls.auth = ETradeAuth(cls.env)
        cls.auth.set_auth_components()
        webbrowser.open(cls.auth.authorize_url)
        cls.verification_code = input('Enter verification code: ')
        cls.auth.make_session(cls.verification_code)

    def testInit(self):
        market = ETradeMarket(self.auth)
        self.assertIsInstance(market.auth, ETradeAuth)


if __name__ == '__main__':
    ut.main()
