from ag95 import (TrailingDecision,
                  MessagesTrailingDecision)
from pprint import pformat
import unittest

class TestTrailingDecision(unittest.TestCase):

    # ########################
    # sanity checks
    # ########################
    def test_case_0001(self):
        input_data = {
            'price_history': [],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': None,
            'reason': MessagesTrailingDecision.INVALID_PRICE_HISTORY
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0003(self):
        input_data = {
            'price_history': [1, 1.1, 1.2],
            'position_price': 1,
            'start_trailing_unit': -0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': None,
            'reason': MessagesTrailingDecision.INVALID_START_UNIT
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0004(self):
        input_data = {
            'price_history': [1, 1.1, 1.2],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': -0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': None,
            'reason': MessagesTrailingDecision.INVALID_END_UNIT
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0005(self):
        input_data = {
            'price_history': [1, 1.1, 1.2],
            'position_price': 1,
            'start_trailing_unit': -0.1,
            'end_trailing_unit': -0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': None,
            'reason': MessagesTrailingDecision.INVALID_START_UNIT
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0006(self):
        input_data = {
            'price_history': [1, 1.1, 1.2],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UPY'
        }
        expected_output = {
            'decision': None,
            'reason': MessagesTrailingDecision.INVALID_DIRECTION
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0007(self):
        input_data = {
            'price_history': [1, 1.1, 1.2],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWNL'
        }
        expected_output = {
            'decision': None,
            'reason': MessagesTrailingDecision.INVALID_DIRECTION
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0008(self):
        input_data = {
            'price_history': [1, 1.1, 1.2],
            'position_price': 1,
            'start_trailing_unit': -0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UPY'
        }
        expected_output = {
            'decision': None,
            'reason': MessagesTrailingDecision.INVALID_START_UNIT
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    # ########################
    # check the UP direction
    # ########################
    # invalid end trailing case
    def test_case_0011(self):
        input_data = {
            'price_history': [1, 1.1, 1.0451],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0012(self):
        input_data = {
            'price_history': [1, 1.1, 1.046],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0013(self):
        input_data = {
            'price_history': [1, 1.1, 1.055],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    # valid end trailing case
    def test_case_0014(self):
        input_data = {
            'price_history': [1, 1.1, 1.045],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    # standby case
    def test_case_0015(self):
        input_data = {
            'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.01, 0.99, 0.7, 0.5],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.STANDBY_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0016(self):
        input_data = {
            'price_history': [0.8, 0.85, 0.9, 1.08, 1.045, 1.01, 0.99, 0.7, 0.5],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.STANDBY_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0017(self):
        input_data = {
            'price_history': [0.8, 0.85, 0.9, 0.95],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.STANDBY_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    # safety net case
    def test_case_0018(self):
        input_data = {
            'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.1, 1.01, 0.99, 0.7, 0.5],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0019(self):
        input_data = {
            'price_history': [0.8, 0.85, 0.9, 1.08, 1.045, 1.01, 0.99, 0.7, 1.1, 0.5],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0020(self):
        input_data = {
            'price_history': [0.5, 0.8, 1.1, 1.02],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    # ########################
    # check the DOWN direction
    # ########################
    # invalid end trailing case
    def test_case_0023(self):
        input_data = {
            'price_history': [1, 0.9, 0.9449],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0024(self):
        input_data = {
            'price_history': [1, 0.9, 0.944],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0025(self):
        input_data = {
            'price_history': [1, 0.9, 0.935],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    # valid end trailing case
    def test_case_0026(self):
        input_data = {
            'price_history': [1, 0.9, 0.945],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    # standby case
    def test_case_0027(self):
        input_data = {
            'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.01],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.STANDBY_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0028(self):
        input_data = {
            'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.1, 1.2, 1.3, 0.91, 0.905],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.STANDBY_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0029(self):
        input_data = {
            'price_history': [1, 2, 3, 4],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.STANDBY_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    # safety net case
    def test_case_0030(self):
        input_data = {
            'price_history': [1, 1.01, 0.9, 1.05, 1.08, 1.045, 1.01],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0031(self):
        input_data = {
            'price_history': [1, 1.01, 0.9, 1.05, 1.08, 1.045, 1.01, 0.95],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    def test_case_0032(self):
        input_data = {
            'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.1, 1.2, 0.9, 1.3, 0.91, 0.905],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0033(self):
        input_data = {
            'price_history': [1, 2, 3, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    # extra random tests
    def test_case_0034(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0036(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 0.85169464],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0037(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826288, 0.85069463],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'DOWN'
        }
        expected_output = {
            'decision': True,
            'reason': MessagesTrailingDecision.TRAILING_END_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    def test_case_0039(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.199912, 1.15421464],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    def test_case_0040(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421465],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0041(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421464, 1.1195882008],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0042(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421464, 1.1195882007],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(result['decision'], expected_output['decision'], f'full result: {result}')
        self.assertEqual(result['reason'], expected_output['reason'], f'full result: {result}')

    def test_case_0043(self):
        input_data = {
            'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421464, 1.1195882009],
            'position_price': 1.0084,
            'start_trailing_unit': 0.18,
            'end_trailing_unit': 0.03,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.SAFETY_NET_CASE
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    def test_case_0044(self):
        input_data = {
            'price_history': [1, 5, 3, 4, 2],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': True,
            'reason': MessagesTrailingDecision.TRAILING_END_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

    def test_case_0045(self):
        input_data = {
            'price_history': [1, 10],
            'position_price': 1,
            'start_trailing_unit': 0.1,
            'end_trailing_unit': 0.05,
            'direction': 'UP'
        }
        expected_output = {
            'decision': False,
            'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED
        }
        result = TrailingDecision(**input_data).take()
        self.assertEqual(expected_output['decision'], result['decision'], f'full result: {pformat(result)}')
        self.assertEqual(expected_output['reason'], result['reason'], f'full result: {pformat(result)}')

if __name__ == '__main__':
    unittest.main(verbosity=2)