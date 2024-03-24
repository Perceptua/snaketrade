from datetime import datetime
from snaketrade.snaketradeutils import SnakeTradeUtils as stu
import json
import requests
import unittest as ut


class TestSnakeTradeUtils(ut.TestCase):
    @classmethod
    def getValueTypes(cls, dataframe):
        first_row = dataframe.loc[0]
        value_types = [type(i) for i in first_row]

        return value_types

    def testParseResponseJSON(self):
        valid_url = 'https://api.github.com/users/perceptua/repos'
        invalid_url = 'https://api.github.com/nonsense'

        response = requests.get(valid_url)
        data = stu.parse_response_json(response)
        self.assertTrue(type(data) == dict or type(data) == list)

        response = requests.get(invalid_url)
        self.assertRaises(ValueError, stu.parse_response_json, response)

    def testDictToDataframe(self):
        sample_json = 'tests/data/sample_balance_response_prod.json'
        sample_data = json.load(open(sample_json))['BalanceResponse']
        dataframe = stu.dict_to_dataframe(sample_data, flatten=True)
        expected_shape = (1, 32)
        value_types = self.getValueTypes(dataframe)
        self.assertEqual(dataframe.shape, expected_shape)
        self.assertNotIn(dict, value_types)

        dataframe = stu.dict_to_dataframe(sample_data, flatten=False)
        expected_shape = (1, 9)
        value_types = self.getValueTypes(dataframe)
        self.assertEqual(dataframe.shape, expected_shape)
        self.assertIn(dict, value_types)

        sample_json = 'tests/data/sample_portfolio_response_prod.json'
        sample_data = json.load(open(sample_json))['PortfolioResponse']
        sample_data = sample_data['AccountPortfolio'][0]['Position'][0]
        dataframe = stu.dict_to_dataframe(sample_data, flatten=True)
        self.assertNotIn(True, dataframe.columns.duplicated())

        dataframe = stu.dict_to_dataframe(
            sample_data, flatten=True, drop_duplicate_columns=False
        )

        self.assertIn(True, dataframe.columns.duplicated())

    def testDictToDataframeList(self):
        sample_json = 'tests/data/sample_transaction_list_response_prod.json'
        sample_data = json.load(open(sample_json))['TransactionListResponse']
        dataframe = stu.dict_to_dataframe(sample_data, flatten=True)
        value_types = self.getValueTypes(dataframe)
        self.assertIn(list, value_types)

    def testCheckDateFormat(self):
        date_str = '02192024'
        fmt_str = '%m%d%Y'
        matches_format = stu.check_date_format(date_str, fmt_str, False)
        self.assertTrue(matches_format)

        fmt_str = '%Y-%m-%d'
        matches_format = stu.check_date_format(date_str, fmt_str, False)
        self.assertFalse(matches_format)

        self.assertRaises(
            Exception, stu.check_date_format, date_str, fmt_str, True
        )

    def testUTCFromMilliseconds(self):
        date_str = '1711027936000'
        utc_timestamp = stu.utc_from_milliseconds(date_str)
        self.assertIsInstance(utc_timestamp, datetime)

        date_str = '2024-03-21 15:54:00.000'
        self.assertRaises(ValueError, stu.utc_from_milliseconds, date_str)


if __name__ == '__main__':
    ut.main()
