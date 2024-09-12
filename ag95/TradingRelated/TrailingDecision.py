from typing import (List,
                    Literal)
from decimal import Decimal
from logging import getLogger
from dataclasses import dataclass
from ag95.LoggingScripts.custom_logger import configure_logger

@dataclass
class MessagesTrailingDecision:
    invalid_start_trailing_unit: str = 'invalid start trailing_unit'
    invalid_end_trailing_unit: str = 'invalid end trailing unit'
    invalid_direction: str = 'invalid direction'
    invalid_price_history: str = 'invalid price history'

    only_last_value_case: str = 'only last value fulfilled'
    standby_case: str = 'in standby mode'

    trailing_end_fulfilled: str = 'trailing end condition fulfilled'
    trailing_end_not_fulfilled: str = 'trailing end condition NOT fulfilled'

class TrailingDecision:
    def __init__(self,
                 price_history: List[int | float | str | Decimal],
                 position_price: int | float | str | Decimal,
                 start_trailing_unit: int | float | str | Decimal,
                 end_trailing_unit: int | float | str | Decimal,
                 direction: Literal['UP', 'DOWN']):

        self._log = getLogger('TrailingDecision')

        # str() is needed here otherwise Decimal would have strange/ inexact values
        self.price_history = [Decimal(str(_)) for _ in price_history]
        self.position_price = Decimal(str(position_price))
        self.start_trailing_unit = Decimal(str(start_trailing_unit))
        self.end_trailing_unit = Decimal(str(end_trailing_unit))
        self.direction = direction

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

        if self.direction not in ['UP', 'DOWN']:
            return [False, MessagesTrailingDecision.invalid_direction]

        return [True, '']

    def _check_limit_reached(self) -> bool:
        '''
        check if the limit was reached or not
        '''

        if self.direction == 'UP':
            return any([_ >= (self.position_price + self.start_trailing_unit * self.position_price) for _ in self.price_history])
        elif self.direction == 'DOWN':
            return any([_ <= (self.position_price - self.start_trailing_unit * self.position_price) for _ in self.price_history])

    def _trailing_mode(self) -> dict:
        '''
        trailing mode
        '''

        # split the price history starting from the position where the limit was reached
        price_history_copy_reverse = self.price_history.copy()
        price_history_copy_reverse.reverse()

        index_reverse_split = None
        for index, _ in enumerate(price_history_copy_reverse):
            if self.direction == 'UP':
                if _ >= self.position_price + self.start_trailing_unit * self.position_price:
                    index_reverse_split = index
                    break
            elif self.direction == 'DOWN':
                if _ <= self.position_price - self.start_trailing_unit * self.position_price:
                    index_reverse_split = index
                    break

        # if index_reverse_split is 0, it means that only the last value
        # meets the limit criteria => return False. no need to execute the following code
        if index_reverse_split == 0:
            self._log.info('Only the last value of the price history fulfills the limit criteria, no need to continue.')
            return {'decision': False,
                    'reason': MessagesTrailingDecision.only_last_value_case}

        price_history = self.price_history[-index_reverse_split-1:]

        # all conditions are valid now => checking if the end limit was reached
        if self.direction == 'UP':
            new_start_limit = max(price_history)
            end_limit_absolute = new_start_limit - new_start_limit * self.end_trailing_unit
            decision = price_history[-1] <= end_limit_absolute

        elif self.direction == 'DOWN':
            new_start_limit = min(price_history)
            end_limit_absolute = new_start_limit + new_start_limit * self.end_trailing_unit
            decision = price_history[-1] >= end_limit_absolute

        if decision:
            self._log.info('Decided that an order should be made.')
            return {'decision': True,
                    'reason': MessagesTrailingDecision.trailing_end_fulfilled}
        else:
            self._log.info('Decided that an order should NOT be made.')
            return {'decision': False,
                    'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}

    def take(self) -> dict:
        checks = self._sanity_checks()
        if not checks[0]:
            self._log.error(f'Failed sanity checks {checks[1]} !!')
            return {'decision': None,
                    'reason': checks[1]}
        else:
            if self._check_limit_reached():
                self._log.info('Limit reached, we are in the "following" mode.')

                return self._trailing_mode()

            else:
                self._log.info('Limit NOT reached, we are in the standby mode.')
                return {'decision': False,
                        'reason': MessagesTrailingDecision.standby_case}

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
          'direction': 'UP'}, {'decision': None,
                                'reason': MessagesTrailingDecision.invalid_price_history}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': -0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': None,
                                'reason': MessagesTrailingDecision.invalid_start_trailing_unit}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': -0.05,
          'direction': 'UP'}, {'decision': None,
                                'reason': MessagesTrailingDecision.invalid_end_trailing_unit}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': -0.1,
          'end_trailing_unit': -0.05,
          'direction': 'UP'}, {'decision': None,
                                'reason': MessagesTrailingDecision.invalid_start_trailing_unit}],

        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UPY'}, {'decision': None,
                                 'reason': MessagesTrailingDecision.invalid_direction}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWNL'}, {'decision': None,
                                  'reason': MessagesTrailingDecision.invalid_direction}],
        [{'price_history': [1, 1.1, 1.2],
          'position_price': 1,
          'start_trailing_unit': -0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UPY'}, {'decision': None,
                                 'reason': MessagesTrailingDecision.invalid_start_trailing_unit}],

        # ########################
        # check the UP direction
        # ########################
        # check the last value limit case
        [{'price_history': [1, 1.1],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': False,
                                'reason': MessagesTrailingDecision.only_last_value_case}],

        # invalid end trailing case
        [{'price_history': [1, 1.1, 1.0451],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': False,
                                'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 1.1, 1.046],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': False,
                                'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 1.1, 1.055],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': False,
                                'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],

        # valid end trailing case
        [{'price_history': [1, 1.1, 1.045],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': True,
                                'reason': MessagesTrailingDecision.trailing_end_fulfilled}],

        # standby case
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.01, 0.99, 0.7, 0.5],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': False,
                                'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [0.8, 0.85, 0.9, 1.08, 1.045, 1.01, 0.99, 0.7, 0.5],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': False,
                                'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [0.8, 0.85, 0.9, 0.95],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'UP'}, {'decision': False,
                                'reason': MessagesTrailingDecision.standby_case}],

        # ########################
        # check the DOWN direction
        # ########################
        # check the last value limit case
        [{'price_history': [1, 0.9],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': False,
                                 'reason': MessagesTrailingDecision.only_last_value_case}],

        # invalid end trailing case
        [{'price_history': [1, 0.9, 0.9449],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': False,
                                 'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 0.9, 0.944],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': False,
                                 'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],
        [{'price_history': [1, 0.9, 0.935],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': False,
                                 'reason': MessagesTrailingDecision.trailing_end_not_fulfilled}],

        # valid end trailing case
        [{'price_history': [1, 0.9, 0.945],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': True,
                                 'reason': MessagesTrailingDecision.trailing_end_fulfilled}],

        # standby case
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.01],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': False,
                                 'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [1, 1.01, 1.05, 1.08, 1.045, 1.1, 1.2, 1.3, 0.91, 0.905],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': False,
                                 'reason': MessagesTrailingDecision.standby_case}],
        [{'price_history': [1, 2, 3, 4],
          'position_price': 1,
          'start_trailing_unit': 0.1,
          'end_trailing_unit': 0.05,
          'direction': 'DOWN'}, {'decision': False,
                                 'reason': MessagesTrailingDecision.standby_case}],

    ]:
        result = TrailingDecision(**test[0]).take()
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')