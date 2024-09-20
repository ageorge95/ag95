from typing import (List,
                    Literal)
from decimal import Decimal
from logging import getLogger
from dataclasses import dataclass
from ag95 import configure_logger

@dataclass
class MessagesTrailingDecision:
    invalid_start_trailing_unit: str = 'invalid start trailing_unit'
    invalid_end_trailing_unit: str = 'invalid end trailing unit'
    invalid_direction: str = 'invalid direction'
    invalid_price_history: str = 'invalid price history'
    invalid_safety_net_detector_unit: str = 'invalid safe net detector unit'

    only_last_value_case: str = 'only last value fulfilled'
    standby_case: str = 'in standby mode'
    safety_net_case: str = 'in safety mode'

    trailing_end_fulfilled: str = 'trailing end condition fulfilled'
    trailing_end_not_fulfilled: str = 'trailing end condition NOT fulfilled'

class TrailingDecision:
    def __init__(self,
                 price_history: List[int | float | str | Decimal],
                 position_price: int | float | str | Decimal,
                 start_trailing_unit: int | float | str | Decimal,
                 end_trailing_unit: int | float | str | Decimal,
                 direction: Literal['UP', 'DOWN'],
                 safety_net_detector_unit: int | float | str | Decimal,
                 show_logs: bool = False):
        """
        @param price_history:
            The list containing the history of previous prices. No limits on length.
        @param position_price:
            The starting price.
        @param start_trailing_unit:
            The parameter used to compute the start_trailing absolute value. Specified in units, ex 0.1 (=10%)
        @param end_trailing_unit:
            The parameter used to compute the end_trailing absolute value. Specified in units, ex 0.1 (=10%)
        @param direction:
            The logic can adapt to both DOWN/ UP scenarios;
            For example if the code is used to compute the best buy-in price, the DOWN direction should be specified.
        @param safety_net_detector_unit:
            This safety parameter will prevent bad decisions if the price swings too much;
            Very useful if the specified data is sparse.
        """
        if show_logs:
            self._log = getLogger('TrailingDecision')

        # str() is needed here otherwise Decimal would have strange/ inexact values
        self.price_history = [Decimal(str(_)) for _ in price_history]
        self.position_price = Decimal(str(position_price))
        self.start_trailing_unit = Decimal(str(start_trailing_unit))
        self.end_trailing_unit = Decimal(str(end_trailing_unit))
        self.direction = direction
        self.safety_net_detector_unit = Decimal(str(safety_net_detector_unit))
        self.show_logs = show_logs

        self.absolute_start_trailing = {'UP': self.position_price + self.position_price * self.start_trailing_unit,
                                        'DOWN': self.position_price - self.position_price * self.start_trailing_unit}

    def _sanity_checks(self):
        '''
        various sanity checks, True if no issues were found, False otherwise
        '''

        if not self.price_history:
            return [False, MessagesTrailingDecision.invalid_price_history]

        if self.start_trailing_unit <= Decimal('0'):
            return [False, MessagesTrailingDecision.invalid_start_trailing_unit]

        if self.end_trailing_unit <= Decimal('0'):
            return [False, MessagesTrailingDecision.invalid_end_trailing_unit]

        if self.safety_net_detector_unit <= Decimal('0'):
            return [False, MessagesTrailingDecision.invalid_safety_net_detector_unit]

        if self.direction not in ['UP', 'DOWN']:
            return [False, MessagesTrailingDecision.invalid_direction]

        return [True, '']

    def _check_limit_reached(self) -> bool:
        '''
        check if the limit was reached or not
        '''

        if self.direction == 'UP':
            return any([_ >= self.absolute_start_trailing['UP'] for _ in self.price_history])
        elif self.direction == 'DOWN':
            return any([_ <= self.absolute_start_trailing['DOWN'] for _ in self.price_history])

    def _trailing_mode(self) -> dict:
        '''
        trailing mode
        '''

        # first check if only the last value was fullfilled or not
        if self.direction == 'UP':
            if self.price_history[-1] == self.absolute_start_trailing['UP']:
                return {'decision': False,
                        'reason': MessagesTrailingDecision.only_last_value_case,
                        'extra': {'price_history[-1]': self.price_history[-1],
                                  'absolute_start_trailing_UP': self.absolute_start_trailing['UP']}}
        elif self.direction == 'DOWN':
            if self.price_history[-1] == self.absolute_start_trailing['DOWN']:
                return {'decision': False,
                        'reason': MessagesTrailingDecision.only_last_value_case,
                        'extra': {'price_history[-1]': self.price_history[-1],
                                  'absolute_start_trailing_UP': self.absolute_start_trailing['DOWN']}}

        # split the price history starting from the position where the limit was reached
        price_history_copy_reverse = self.price_history.copy()
        price_history_copy_reverse.reverse()

        for index, _ in enumerate(price_history_copy_reverse):
            if self.direction == 'UP':
                if _ >= self.absolute_start_trailing['UP']:
                    index_reverse_split = index
                    break
            elif self.direction == 'DOWN':
                if _ <= self.absolute_start_trailing['DOWN']:
                    index_reverse_split = index
                    break

        if index_reverse_split != 0:
            self.price_history = self.price_history[-index_reverse_split - 1:]

        # all conditions are valid now => checking if the end limit was reached
        # check if the safet net mode needs to be activated or not
        if self.direction == 'UP':
            new_start_limit = max(self.price_history)
            end_limit_absolute = new_start_limit - new_start_limit * self.end_trailing_unit
            safety_net_limit_absolute = end_limit_absolute - end_limit_absolute * self.safety_net_detector_unit
            decision = self.price_history[-1] <= end_limit_absolute

            if self.price_history[-1] <= safety_net_limit_absolute:
                if self.show_logs:
                    self._log.warning('Safety net mode activated !')
                return {'decision': False,
                        'reason': MessagesTrailingDecision.safety_net_case,
                        'extra': {'new_start_limit': new_start_limit,
                                  'end_limit_absolute': end_limit_absolute,
                                  'safety_net_limit_absolute': safety_net_limit_absolute,
                                  'position_price': self.position_price,
                                  'price_history[-1]': self.price_history[-1]}}

        elif self.direction == 'DOWN':
            new_start_limit = min(self.price_history)
            end_limit_absolute = new_start_limit + new_start_limit * self.end_trailing_unit
            safety_net_limit_absolute = end_limit_absolute + end_limit_absolute * self.safety_net_detector_unit
            decision = self.price_history[-1] >= end_limit_absolute

            if self.price_history[-1] >= safety_net_limit_absolute:
                if self.show_logs:
                    self._log.warning('Safety net mode activated !')
                return {'decision': False,
                        'reason': MessagesTrailingDecision.safety_net_case,
                        'extra': {'new_start_limit': new_start_limit,
                                  'end_limit_absolute': end_limit_absolute,
                                  'safety_net_limit_absolute': safety_net_limit_absolute,
                                  'position_price': self.position_price,
                                  'price_history[-1]': self.price_history[-1]}}

        if decision:
            if self.show_logs:
                self._log.info('Decided that an order should be made.')
            return {'decision': True,
                    'reason': MessagesTrailingDecision.trailing_end_fulfilled,
                    'extra': {'new_start_limit': new_start_limit,
                              'end_limit_absolute': end_limit_absolute,
                              'safety_net_limit_absolute': safety_net_limit_absolute,
                              'position_price': self.position_price,
                              'price_history[-1]': self.price_history[-1]}}
        else:
            if self.show_logs:
                self._log.info('Decided that an order should NOT be made.')
            return {'decision': False,
                    'reason': MessagesTrailingDecision.trailing_end_not_fulfilled,
                    'extra': {'new_start_limit': new_start_limit,
                              'end_limit_absolute': end_limit_absolute,
                              'safety_net_limit_absolute': safety_net_limit_absolute,
                              'position_price': self.position_price,
                              'price_history[-1]': self.price_history[-1]}}

    def take(self) -> dict:
        checks = self._sanity_checks()
        if not checks[0]:
            if self.show_logs:
                self._log.error(f'Failed sanity checks {checks[1]} !!')
            return {'decision': None,
                    'reason': checks[1],
                    'extra': {}}
        else:
            if self._check_limit_reached():
                if self.show_logs:
                    self._log.info('Limit reached, we are in the "following" mode.')

                return self._trailing_mode()

            else:
                if self.show_logs:
                    self._log.info('Limit NOT reached, we are in the standby mode.')
                return {'decision': False,
                        'reason': MessagesTrailingDecision.standby_case,
                        'extra': {}}

if __name__ == '__main__':

    configure_logger()

    for test in [
        # ########################
        # sanity checks
        # ########################
        [{'price_history': [],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_price_history}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': -0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_safety_net_detector_unit}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': -0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_start_trailing_unit}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': -0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_end_trailing_unit}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': -0.1,
          'end_trailing_unit': -0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_start_trailing_unit}],

        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UPY',
          'safety_net_detector_unit': 0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_direction}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWNL',
          'safety_net_detector_unit': 0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_direction}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': -0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UPY',
          'safety_net_detector_unit': 0.03}, {'decision': None,
                                              'reason': MessagesTrailingDecision.invalid_start_trailing_unit}],

        # ########################
        # check the UP direction
        # ########################
        # check the last value limit case
        [{'price_history': [1, 1.1],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.only_last_value_case}],
        [{'price_history': [1, 1.01, 1.02, 1.03, 1.04, 1.05, 1.1, 1.1],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.only_last_value_case}],

        # invalid end trailing case
        [{'price_history': [1, 1.1, 1.0451],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 1.1, 1.046],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 1.1, 1.055],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],

        # valid end trailing case
        [{'price_history': [1, 1.1, 1.045],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],

        # standby case
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.01, 0.99, 0.7, 0.5],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [0.8, 0.85, 0.9, 1.08, 1.045, 1.01, 0.99, 0.7, 0.5],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [0.8, 0.85, 0.9, 0.95],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.standby_case}],

        # safety net case
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.1, 1.01, 0.99, 0.7, 0.5],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.safety_net_case}],
        [{'price_history': [0.8, 0.85, 0.9, 1.08, 1.045, 1.01, 0.99, 0.7, 1.1, 0.5],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.safety_net_case}],
        [{'price_history': [0.5, 0.8, 1.1, 1.02],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],

        # ########################
        # check the DOWN direction
        # ########################
        # check the last value limit case
        [{'price_history': [1, 0.9],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.only_last_value_case}],
        [{'price_history': [1, 0.99, 0.98, 0.97, 0.96, 0.95, 0.9],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.only_last_value_case}],

        # invalid end trailing case
        [{'price_history': [1, 0.9, 0.9449],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 0.9, 0.944],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 0.9, 0.935],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],

        # valid end trailing case
        [{'price_history': [1, 0.9, 0.945],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],

        # standby case
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.01],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.1, 1.2, 1.3, 0.91, 0.905],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [1, 2, 3, 4],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.standby_case}],

        # safety net case
        [{'price_history': [1, 1.01, 0.9, 1.05, 1.08, 1.045, 1.01],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.safety_net_case}],
        [{'price_history': [1, 1.01, 0.9, 1.05, 1.08, 1.045, 1.01, 0.95],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.1, 1.2, 0.9, 1.3, 0.91, 0.905],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 2, 3, 0.9, 0.91, 0.92, 0.93, 0.94, 0.95],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],

        # extra random tests
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.only_last_value_case}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 0.85169464],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 0.85169463],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'DOWN',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.only_last_value_case}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421464],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421465],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421464, 1.1195882008],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.safety_net_case}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421464, 1.1195882007],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': False,
                                              'reason': MessagesTrailingDecision.safety_net_case}],
        [{'price_history': [0.8226, 0.8197, 0.8049, 0.7994, 0.7997, 0.826888, 1.189912, 1.15421464, 1.1195882009],
          'position_price': 1.0084,
          'start_trailing_unit': 0.18,
          'end_trailing_unit': 0.03,
          'direction': 'UP',
          'safety_net_detector_unit': 0.03}, {'decision': True,
                                              'reason': MessagesTrailingDecision.trailing_end_fulfilled}],

    ]:
        result = TrailingDecision(**test[0]).take()
        assert result['decision'] == test[1]['decision'] and result['reason'] == test[1]['reason'] ,\
            f"invalid function return for" \
            f"\n\tinput: {test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')

    # quick check, uncomment and modify
    # from pprint import pprint
    # pprint(TrailingDecision(price_history=[73.1],
    #                         position_price=89.4,
    #                         start_trailing_unit=0.18,
    #                         end_trailing_unit=0.03,
    #                         direction='DOWN',
    #                         safety_net_detector_unit=0.03).take())