from snaketrade.snaketradeutils import SnakeTradeUtils as stu
import unittest as ut


class TestSnakeTradeUtils(ut.TestCase):
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


if __name__ == '__main__':
    ut.main()
