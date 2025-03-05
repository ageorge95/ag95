from typing import (List,
                    Literal,
                    Tuple,
                    Union)
from decimal import Decimal
from logging import getLogger
from dataclasses import dataclass

@dataclass
class MessagesTrailingDecision:
    INVALID_START_UNIT: str = 'Invalid start trailing unit'
    INVALID_END_UNIT: str = 'Invalid end trailing unit'
    INVALID_DIRECTION: str = 'Invalid direction'
    INVALID_PRICE_HISTORY: str = 'Invalid price history'
    INVALID_SAFETY_NET_UNIT: str = 'Invalid safety net detector unit'

    ONLY_LAST_VALUE_CASE: str = 'Only last value fulfilled'
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
                 safety_net_detector_unit: Union[int, float, str, Decimal],
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
        safety_net_detector_unit : int, float, str, Decimal
            Safety parameter to prevent bad decisions if the price swings too much.
        show_logs : bool, optional
            Enable logging if set to True.
        """
        self.price_history = [Decimal(str(_)) for _ in price_history]
        self.position_price = Decimal(str(position_price))
        self.start_trailing_unit = Decimal(str(start_trailing_unit))
        self.end_trailing_unit = Decimal(str(end_trailing_unit))
        self.direction = direction
        self.safety_net_detector_unit = Decimal(str(safety_net_detector_unit))
        self.show_logs = show_logs

        if show_logs:
            self._log = getLogger('TrailingDecision')
            self._log.setLevel('INFO')

        self.absolute_start_trailing = {
            'UP': self.position_price * (1 + self.start_trailing_unit),
            'DOWN': self.position_price * (1 - self.start_trailing_unit)
        }

    def _sanity_checks(self) -> Tuple[bool, str]:
        if not self.price_history:
            return False, MessagesTrailingDecision.INVALID_PRICE_HISTORY

        if self.start_trailing_unit <= Decimal('0'):
            return False, MessagesTrailingDecision.INVALID_START_UNIT

        if self.end_trailing_unit <= Decimal('0'):
            return False, MessagesTrailingDecision.INVALID_END_UNIT

        if self.safety_net_detector_unit <= Decimal('0'):
            return False, MessagesTrailingDecision.INVALID_SAFETY_NET_UNIT

        if self.direction not in ['UP', 'DOWN']:
            return False, MessagesTrailingDecision.INVALID_DIRECTION

        return True, ''

    def _check_limit_reached(self) -> bool:
        target = self.absolute_start_trailing[self.direction]
        return any((_ >= target if self.direction == 'UP' else _ <= target) for _ in self.price_history)

    def _calculate_trailing_limits(self, new_start_limit: Decimal) -> Tuple[Decimal, Decimal]:
        if self.direction == 'UP':
            end_limit = new_start_limit * (1 - self.end_trailing_unit)
            safety_net_limit = end_limit * (1 - self.safety_net_detector_unit)
        else:  # DOWN direction
            end_limit = new_start_limit * (1 + self.end_trailing_unit)
            safety_net_limit = end_limit * (1 + self.safety_net_detector_unit)
        return end_limit, safety_net_limit

    def _trailing_mode(self) -> dict:
        price = self.price_history[-1]
        if self.direction == 'UP' and price == self.absolute_start_trailing['UP'] or \
           self.direction == 'DOWN' and price == self.absolute_start_trailing['DOWN']:
            return {
                'decision': False,
                'reason': MessagesTrailingDecision.ONLY_LAST_VALUE_CASE,
                'extra': self.extra_return
            }

        # Dynamically adjust the trailing start point
        if self.direction == 'UP':
            new_start_limit = max(max(self.price_history), self.absolute_start_trailing['UP'])
        else:  # DOWN direction
            new_start_limit = min(min(self.price_history), self.absolute_start_trailing['DOWN'])

        end_limit, safety_net_limit = self._calculate_trailing_limits(new_start_limit)
        decision = price <= end_limit if self.direction == 'UP' else price >= end_limit

        if (price <= safety_net_limit if self.direction == 'UP' else price >= safety_net_limit):
            if self.show_logs:
                self._log.warning('Safety net mode activated!')
            return {
                'decision': False,
                'reason': MessagesTrailingDecision.SAFETY_NET_CASE,
                'extra': self.extra_return | {
                    'new_start_limit': new_start_limit,
                    'end_limit': [end_limit,
                                  f'{new_start_limit}'
                                  f'{'-' if self.direction == 'UP' else '+'}'
                                  f'({new_start_limit}*{self.safety_net_detector_unit})'],
                    'safety_net_limit': [safety_net_limit,
                                         f'{end_limit}'
                                         f'{'-' if self.direction == 'UP' else '+'}'
                                         f'{self.safety_net_detector_unit}']
                }
            }

        return {
            'decision': decision,
            'reason': MessagesTrailingDecision.TRAILING_END_FULFILLED if decision else MessagesTrailingDecision.TRAILING_END_NOT_FULFILLED,
            'extra': self.extra_return | {
                'new_start_limit': new_start_limit,
                'end_limit': [end_limit,
                              f'{new_start_limit}'
                              f'{'-' if self.direction == 'UP' else '+'}'
                              f'({new_start_limit}*{self.safety_net_detector_unit})'],
                'safety_net_limit': [safety_net_limit,
                                     f'{end_limit}'
                                     f'{'-' if self.direction == 'UP' else '+'}'
                                     f'{self.safety_net_detector_unit}']
            }
        }

    def take(self) -> dict:
        valid, reason = self._sanity_checks()
        if valid:
            self.extra_return = {
                'price_history[-1]': self.price_history[-1],
                'initial_absolute_start_trailing': [self.absolute_start_trailing[self.direction],
                                                    f'{self.position_price}'
                                                    f'*(1{'+' if self.direction == 'UP' else '-'}{self.start_trailing_unit})'],
                'position_price': self.position_price
            }
        else:
            self.extra_return = {
                'position_price': self.position_price
            }

        if not valid:
            if self.show_logs:
                self._log.error(f'Failed sanity checks: {reason}')
            return {
                'decision': None,
                'reason': reason,
                'extra': self.extra_return
            }

        if self._check_limit_reached():
            if self.show_logs:
                self._log.info('Limit reached, following mode.')
            return self._trailing_mode()

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
                               'direction': 'DOWN',
                               'safety_net_detector_unit': 0.03}).take())