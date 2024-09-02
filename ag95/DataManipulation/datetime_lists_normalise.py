from typing import (List,
                    Dict,
                    Literal,
                    Callable)
from datetime import (datetime,
                      timedelta)

def datetime_lists_normalise(datetime_lists: List[List[Dict]],
                             max_deviation_ms: float | int = 50,
                             supress_sanity_check_messages: bool = False,
                             sort: Literal['ASC', 'DESC', 'NONE'] = 'ASC',
                             custom_function_step: Callable = None,
                             custom_function_total: Callable = None) -> List[Dict]:

    # some sanity checks first
    sanity_fail = [False, '']
    if not isinstance(datetime_lists, list):
        sanity_fail = [True, 'input is not a list']
    elif not all([isinstance(_, list) for _ in datetime_lists]):
        sanity_fail = [True, 'the elements of input are not a list']
    elif not all([isinstance(__, dict) for _ in datetime_lists for __ in _]):
        sanity_fail =[True, 'the elements of elements of input are not a dict']
    if sanity_fail[0]:
        if not supress_sanity_check_messages:
            print(f'input invalid: {sanity_fail[1]} !!!')
        return None

    # make a list with all the unique datetimes
    all_unique_datetimes = set()
    for sublist in datetime_lists:
        for object in sublist:
            all_unique_datetimes.add(list(object.keys())[0]) # the only key for the dict object must be a datetime object

    # sort all_unique_datetimes if requested
    if sort != 'NONE':
        all_unique_datetimes = sorted(all_unique_datetimes, reverse=False if sort == 'ASC' else True)

    # iterate through all possible datetimes and construct the final returned object
    final_return = []
    sublists_len = len(datetime_lists)

    for main_key in all_unique_datetimes:
        to_append = []
        deviation_comparison = [main_key-timedelta(milliseconds=max_deviation_ms), main_key+timedelta(milliseconds=max_deviation_ms)]

        for sublist in datetime_lists:
            for object in sublist:
                relevant_datetime = list(object.keys())[0]
                if deviation_comparison[0] <= relevant_datetime <= deviation_comparison[1]:

                    # execute a custom function, if provided, on each step
                    if custom_function_step:
                        to_append.append([*object.values(), custom_function_step(*object.values())])
                    else:
                        to_append.append(*object.values())

                    break # if a good value is found stop looking into the rest of the sublist

        if len(to_append) == sublists_len: # only add the new element if suitable values were found in all sublists
            # execute a custom function, if provided, on the total data
            if custom_function_total:
                final_return.append({main_key: [to_append, custom_function_total(to_append)]})
            else:
                final_return.append({main_key: to_append})

    return final_return

if __name__ == '__main__':

    now = datetime.now()

    for test in [
        # check the sanity check invalidity
        [{'datetime_lists': [{now: 1}],
          'supress_sanity_check_messages': True}, None],
        [{'datetime_lists': [{now-timedelta(seconds=60): 1}, {now: 2}],
          'supress_sanity_check_messages': True}, None],
        [{'datetime_lists': [{now-timedelta(seconds=60): 564,
                              now: 1}],
          'supress_sanity_check_messages': True}, None],
        [{'datetime_lists': [[1,2,3]],
          'supress_sanity_check_messages': True}, None],
        [{'datetime_lists': [[[1, 2, 3]]],
          'supress_sanity_check_messages': True}, None],

        # check the correct normalisation
        [{'datetime_lists': [[{now: 1}]]}, [{now: [1]}]],
        [{'datetime_lists': [[{now-timedelta(seconds=60): 1}, {now: 2}],
                             [{now-timedelta(seconds=60): 3}, {now: 4}]]},
                            [{now-timedelta(seconds=60): [1,3]},
                             {now: [2,4]}]],

        # check the correct normalisation in reverse
        [{'datetime_lists': [[{now: 1}]],
          'sort': 'DESC'}, [{now: [1]}]],
        [{'datetime_lists': [[{now-timedelta(seconds=60): 1}, {now: 2}],
                             [{now-timedelta(seconds=60): 3}, {now: 4}]],
          'sort': 'DESC'},
                            [{now: [2,4]},
                             {now-timedelta(seconds=60): [1,3]}]],

        # check the edge cases where the max deviation is not fulfilled
        [{'datetime_lists': [[{now: 1}]],
          'max_deviation_ms': 0}, [{now: [1]}]],
        [{'datetime_lists': [[{now-timedelta(seconds=60): 1}, {now: 2}],
                             [{now-timedelta(seconds=60): 3}, {now: 4}]],
          'max_deviation_ms': 0},
                            [{now-timedelta(seconds=60): [1,3]},
                             {now: [2,4]}]],

        [{'datetime_lists': [[{now: 1}]],
          'max_deviation_ms': 50}, [{now: [1]}]],
        [{'datetime_lists': [[{now-timedelta(seconds=60): 1}, {now: 2}],
                             [{now-timedelta(seconds=60): 3}, {now: 4}]],
          'max_deviation_ms': 50},
                            [{now-timedelta(seconds=60): [1,3]},
                             {now: [2,4]}]],

        [{'datetime_lists': [[{now-timedelta(milliseconds=101): 1}],
                             [{now-timedelta(milliseconds=50): 2}]],
          'max_deviation_ms': 50},
                            []],
        [{'datetime_lists': [[{now-timedelta(milliseconds=101): 1}],
                             [{now-timedelta(milliseconds=30): 2}]],
          'max_deviation_ms': 50},
                            []],
        [{'datetime_lists': [[{now-timedelta(milliseconds=100): 1}],
                             [{now-timedelta(milliseconds=50): 2}]],
          'max_deviation_ms': 50},
                            [{now-timedelta(milliseconds=100): [1,2]},
                             {now-timedelta(milliseconds=50): [1,2]}]],
        [{'datetime_lists': [[{now-timedelta(milliseconds=100): 1}],
                             [{now-timedelta(milliseconds=70): 2}]],
          'max_deviation_ms': 50},
                            [{now-timedelta(milliseconds=100): [1,2]},
                             {now-timedelta(milliseconds=70): [1,2]}]],

        # try more complex sublists
        [{'datetime_lists': [[{now-timedelta(minutes=5): 1}, {now-timedelta(minutes=3): 2},
                              {now-timedelta(minutes=2): 3}, {now-timedelta(minutes=1): 4}, {now: 5}],

                            [{now-timedelta(minutes=4): 6}, {now-timedelta(minutes=2): 7},
                             {now-timedelta(minutes=1): 8}, {now: 9}]]},

                            [{now-timedelta(minutes=2): [3,7]},
                             {now-timedelta(minutes=1): [4,8]},
                             {now: [5,9]}]],

        [{'datetime_lists': [[{now-timedelta(minutes=5): 1}, {now-timedelta(minutes=3): 2},
                              {now-timedelta(minutes=2): 3}, {now-timedelta(minutes=1): 4}, {now: 5}],

                            [{now-timedelta(minutes=4): 6}, {now-timedelta(minutes=2): 7},
                             {now-timedelta(minutes=1): 8}, {now: 9}],

                            [{now-timedelta(minutes=4): 10}, {now-timedelta(minutes=2): [11]},
                             {now-timedelta(minutes=1): [12,786]}, {now: 13}]]},

                            [{now-timedelta(minutes=2): [3,7,[11]]},
                             {now-timedelta(minutes=1): [4,8,[12,786]]},
                             {now: [5,9,13]}]],

        # check the custom step function
        [{'datetime_lists': [[{now: 1}]],
          'custom_function_step': lambda x:x+1}, [{now: [[1,2]]}]],
        [{'datetime_lists': [[{now-timedelta(minutes=4): 10}, {now: 1}]],
          'custom_function_step': lambda x: x + 1}, [{now-timedelta(minutes=4): [[10,11]]}, {now: [[1, 2]]}]],

        # check the custom final function
        [{'datetime_lists': [[{now: 1}]],
          'custom_function_total': lambda x: x + ['extra_stuff']}, [{now: [[1], [1, 'extra_stuff']]}]],
        [{'datetime_lists': [[{now: 1}]],
          'custom_function_total': lambda x: ['extra_stuff']}, [{now: [[1], ['extra_stuff']]}]],
    ]:
        result = datetime_lists_normalise(**test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')