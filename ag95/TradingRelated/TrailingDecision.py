from typing import (List,
                    Literal,
                    Tuple,
                    Union)
from decimal import Decimal
from logging import getLogger
from dataclasses import dataclass
from collections import OrderedDict

@dataclass
class MessagesTrailingDecision:
    INVALID_START_UNIT: str = 'Invalid start trailing unit'
    INVALID_END_UNIT: str = 'Invalid end trailing unit'
    INVALID_DIRECTION: str = 'Invalid direction'
    INVALID_PRICE_HISTORY: str = 'Invalid price history'
    INVALID_EQUAL_START_END_UNITS: str = 'Invalid equal start and end units'
    INVALID_END_GREATER_THAN_START_UNITS: str = 'Invalid end unit is greater than start unit'

    STANDBY_CASE: str = 'In standby mode'
    SAFETY_NET_CASE: str = 'In safety mode'

    TRAILING_END_FULFILLED: str = 'Trailing end condition fulfilled'
    TRAILING_END_NOT_FULFILLED: str = 'Trailing end condition NOT fulfilled'

class TrailingDecision:
    def __init__(self,
                 price_history: List[Union[int, float, str, Decimal]],
                 position_price: Union[int, float, str, Decimal],
                 start_trailing_unit: Union[int, float, str, Decimal],
                 end_trailing_unit: Union[int, float, str, Decimal],
                 direction: Literal['UP', 'DOWN'],
                 show_logs: bool = False):
        """
        Parameters
        ----------
        price_history : list of int, float, str, Decimal
            The list containing the history of previous prices. No limits on length.
        position_price : int, float, str, Decimal
            The starting price.
        start_trailing_unit : int, float, str, Decimal
            The parameter used to compute the start_trailing absolute value. Specified in units, e.g., 0.1 (=10%).
        end_trailing_unit : int, float, str, Decimal
            The parameter used to compute the end_trailing absolute value. Specified in units, e.g., 0.1 (=10%).
        direction : {'UP', 'DOWN'}
            The logic can adapt to both DOWN/UP scenarios.
        show_logs : bool, optional
            Enable logging if set to True.
        """
        self.price_history = [Decimal(str(_)) for _ in price_history]
        self.position_price = Decimal(str(position_price))
        self.start_trailing_unit = Decimal(str(start_trailing_unit))
        self.end_trailing_unit = Decimal(str(end_trailing_unit))
        self.direction = direction
        self.show_logs = show_logs

        if show_logs:
            self._log = getLogger('TrailingDecision')
            self._log.setLevel('INFO')

    def _sanity_checks(self) -> Tuple[bool, str]:
        if not self.price_history:
            return False, MessagesTrailingDecision.INVALID_PRICE_HISTORY

        if self.start_trailing_unit <= Decimal('0'):
            return False, MessagesTrailingDecision.INVALID_START_UNIT

        if self.end_trailing_unit <= Decimal('0'):
            return False, MessagesTrailingDecision.INVALID_END_UNIT

        if self.start_trailing_unit == self.end_trailing_unit:
            return False, MessagesTrailingDecision.INVALID_EQUAL_START_END_UNITS

        if self.end_trailing_unit > self.start_trailing_unit:
            return False, MessagesTrailingDecision.INVALID_END_GREATER_THAN_START_UNITS

        if self.direction not in ['UP', 'DOWN']:
            return False, MessagesTrailingDecision.INVALID_DIRECTION

        return True, ''

    def _trailing_mode(self) -> dict:
        last_history_price = self.price_history[-1]

        self.adjusted_absolute_start_trailing_value = {
            'UP': max(max(self.price_history), self.initial_absolute_start_trailing_value['UP']),
            'DOWN': min(min(self.price_history), self.initial_absolute_start_trailing_value['DOWN'])
        }
        self.adjusted_absolute_end_trailing_value = {
            'UP': self.adjusted_absolute_start_trailing_value[self.direction] * (1 - self.end_trailing_unit),
            'DOWN': self.adjusted_absolute_start_trailing_value[self.direction] * (1 + self.end_trailing_unit)
        }
        has_reached_end_limit = {
            'UP': last_history_price <= self.adjusted_absolute_end_trailing_value['UP'],
            'DOWN': last_history_price >= self.adjusted_absolute_end_trailing_value['DOWN']
        }
        has_broken_safety_margins = {
            'UP': last_history_price <= self.initial_absolute_end_trailing_value['UP'],
            'DOWN': last_history_price >= self.initial_absolute_end_trailing_value['DOWN']
        }
        self.extra_return |= {
            'adjusted_absolute_start_trailing_value': [self.adjusted_absolute_start_trailing_value[self.direction],
                                                       f'max(max(price_history), '
                                                       f'{self.initial_absolute_start_trailing_value[self.direction]})'],
            'adjusted_absolute_end_trailing_value': [self.adjusted_absolute_end_trailing_value[self.direction],
                                                     f'{self.adjusted_absolute_start_trailing_value[self.direction]}'
                                                     f'*(1{'-' if self.direction == 'UP' else '+'}{self.end_trailing_unit})'],
            'has_reached_end_limit': [has_reached_end_limit[self.direction],
                                      f'{last_history_price}{'<=' if self.direction == 'UP' else '>='}'
                                      f'{self.adjusted_absolute_end_trailing_value[self.direction]}']
        }
        
        if has_reached_end_limit[self.direction]:
            self.extra_return |= {
            'has_broken_safety_margins': [has_broken_safety_margins[self.direction],
                                      f'{last_history_price}{'<=' if self.direction == 'UP' else '>='}'
                                      f'{self.initial_absolute_end_trailing_value[self.direction]}']
        }
            if has_broken_safety_margins[self.direction]:
                return {
                    'decision': False,
                    'reason': MessagesTrailingDecision.SAFETY_NET_CASE,
                    'extra': self.extra_return
                }
            else:
                return {
                    'decision': True,
                    'reason': MessagesTrailingDecision.TRAILING_END_FULFILLED,
                    'extra': self.extra_return
                }
        else:
            return {
                'decision': False,
                'reason': MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED,
                'extra': self.extra_return
            }        

    def take(self) -> dict:
        # first do some sanity checks
        valid, reason = self._sanity_checks()
        if not valid:
            if self.show_logs:
                self._log.error(f'Failed sanity checks: {reason}')
            return {
                'decision': None,
                'reason': reason,
                'extra': 'Failed sanity checks'
            }
        self.extra_return = OrderedDict({
            'price_history[-1]': self.price_history[-1],
            'position_price': self.position_price
        })

        # compute the absolute trailing values based on the input parameters
        self.initial_absolute_start_trailing_value = {
            'UP': self.position_price * (1 + self.start_trailing_unit),
            'DOWN': self.position_price * (1 - self.start_trailing_unit)
        }
        self.initial_absolute_end_trailing_value = {
            'UP': self.initial_absolute_start_trailing_value[self.direction] * (1 - self.end_trailing_unit),
            'DOWN': self.initial_absolute_start_trailing_value[self.direction] * (1 + self.end_trailing_unit)
        }
        has_reached_start_limit = {
            'UP': any([_ >= self.initial_absolute_start_trailing_value['UP'] for _ in self.price_history]),
            'DOWN': any([_ <= self.initial_absolute_start_trailing_value['DOWN'] for _ in self.price_history])
        }
        
        self.extra_return |= {
            'initial_absolute_start_trailing_value': [self.initial_absolute_start_trailing_value[self.direction],
                                                      f'{self.position_price}'
                                                      f'*(1{'+' if self.direction == 'UP' else '-'}{self.start_trailing_unit})'],
            'initial_absolute_end_trailing_value': [self.initial_absolute_end_trailing_value[self.direction],
                                                    f'{self.initial_absolute_start_trailing_value[self.direction]}'
                                                    f'*(1{'-' if self.direction == 'UP' else '+'}{self.end_trailing_unit})'],
            'has_reached_start_limit': [has_reached_start_limit[self.direction],
                                        f'something in price_history'
                                        f'{'>=' if self.direction == 'UP' else '<='}'
                                        f'{self.initial_absolute_start_trailing_value[self.direction]})']
        }

        # check if in trailing mode
        if has_reached_start_limit[self.direction]:
            if self.show_logs:
                self._log.info('Start follow limit reached, going into following mode.')
            return self._trailing_mode()

        # if not in trailing mode return the appropiate values
        if self.show_logs:
            self._log.info('Limit not reached, standby mode.')
        return {
            'decision': False,
            'reason': MessagesTrailingDecision.STANDBY_CASE,
            'extra': self.extra_return
        }

if __name__ == '__main__':

    from pprint import pprint
    pprint(TrailingDecision(**{'price_history': [10],
                               'position_price': 10,
                               'start_trailing_unit': 0.1,
                               'end_trailing_unit': 0.03,
                               'direction': 'DOWN'}).take())