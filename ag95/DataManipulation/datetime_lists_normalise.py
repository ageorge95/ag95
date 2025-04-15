import bisect
from datetime import datetime, timedelta
from typing import List, Dict, Callable, Literal, Any, Tuple

# Helper type for clarity
DateTimeValueTuple = Tuple[datetime, Any]

def datetime_lists_normalise(
    datetime_lists: List[List[Dict]],
    max_deviation_ms: float | int = 50,
    suppress_sanity_check_messages: bool = False,
    sort: Literal['ASC', 'DESC', 'NONE'] = 'ASC',
    custom_function_step: Callable = None,
    custom_function_total: Callable = None
) -> List[Dict] | None:
    """
    Normalises lists of dictionaries based on datetime proximity.

    Finds groups of items (one from each input sublist) where the datetime keys
    are within `max_deviation_ms` of each other, using one datetime as a reference.

    Args:
        datetime_lists: A list containing sublists. Each sublist contains
                        dictionaries. Each dictionary must have exactly one
                        key, which is a datetime object.
        max_deviation_ms: The maximum allowed time difference (in milliseconds)
                          between datetimes in a matching group relative to the
                          reference datetime.
        suppress_sanity_check_messages: If True, suppresses print messages on
                                        input validation failure.
        sort: How to sort the final output based on the reference datetimes.
              'ASC' (ascending), 'DESC' (descending), or 'NONE'.
        custom_function_step: An optional function to apply to each individual
                              value found within a matching group. It receives
                              the original value as input.
        custom_function_total: An optional function to apply to the list of
                               (potentially step-transformed) values collected
                               for a matching group. It receives the list of
                               values as input.

    Returns:
        A list of dictionaries. Each dictionary has a reference datetime as the key.
        The value is a list containing the values from the matching dictionaries
        found across the sublists (potentially transformed by custom_function_step).
        If custom_function_total is provided, the value is a list containing two
        elements: [list_of_values, result_of_custom_function_total].
        Returns None if input sanity checks fail.
    """
    # --- Sanity Checks ---
    sanity_fail = [False, '']
    if not isinstance(datetime_lists, list):
        sanity_fail = [True, 'input is not a list']
    elif not datetime_lists: # Handle empty input list
         sanity_fail = [True, 'input list is empty']
    # Check list types first - slightly more efficient if outer check fails
    elif not all(isinstance(sublist, list) for sublist in datetime_lists):
        sanity_fail = [True, 'one or more elements of input are not lists']
    # Check dict types - combine inner loops for efficiency
    elif not all(isinstance(item, dict)
                 for sublist in datetime_lists
                 for item in sublist):
        sanity_fail = [True, 'one or more elements within sublists are not dicts']
    # Check dict content (single datetime key) - more robust check
    elif not all(len(item) == 1 and isinstance(next(iter(item.keys())), datetime)
                 for sublist in datetime_lists
                 for item in sublist):
         sanity_fail = [True, 'one or more dicts do not contain a single datetime key']

    if sanity_fail[0]:
        if not suppress_sanity_check_messages:
            print(f'Input invalid: {sanity_fail[1]} !!!')
        return None
    # --- End Sanity Checks ---

    # --- Pre-processing ---
    # 1. Extract (datetime, value) pairs and collect unique datetimes
    # 2. Sort each sublist by datetime for efficient searching
    all_unique_datetimes = set()
    processed_lists: List[List[DateTimeValueTuple]] = []
    deviation_delta = timedelta(milliseconds=max_deviation_ms) # Calculate once

    for sublist in datetime_lists:
        processed_sublist: List[DateTimeValueTuple] = []
        for obj_dict in sublist:
            # Assumes valid dict structure from sanity check
            dt_key = next(iter(obj_dict.keys()))
            value = obj_dict[dt_key]
            processed_sublist.append((dt_key, value))
            all_unique_datetimes.add(dt_key)
        # Sort each sublist by datetime
        processed_sublist.sort(key=lambda item: item[0])
        processed_lists.append(processed_sublist)
    # --- End Pre-processing ---

    # Sort all unique datetimes if requested
    # Convert set to list for sorting
    sorted_unique_datetimes = list(all_unique_datetimes)
    if sort != 'NONE':
        sorted_unique_datetimes.sort(reverse=(sort == 'DESC'))

    # --- Main Processing Loop (Optimized with bisect) ---
    final_return = []
    sublists_len = len(processed_lists) # Use count of processed lists

    for main_key in sorted_unique_datetimes:
        to_append = []
        lower_bound = main_key - deviation_delta
        upper_bound = main_key + deviation_delta

        found_in_all = True # Assume success initially
        for sorted_sublist in processed_lists:
            if not sorted_sublist: # Skip empty pre-processed sublists
                found_in_all = False
                break

            # Find the leftmost index where dt >= lower_bound
            # We only need the datetime for bisect_left
            idx_left = bisect.bisect_left(sorted_sublist, lower_bound, key=lambda item: item[0])

            # Check if a suitable item exists within the range
            # The item at idx_left is the first candidate >= lower_bound
            if idx_left < len(sorted_sublist):
                candidate_dt, candidate_value = sorted_sublist[idx_left]
                if candidate_dt <= upper_bound: # Check if it's also <= upper_bound
                    # Match found - process it
                    if custom_function_step:
                        # Pass only the value to the step function
                        to_append.append([candidate_value, custom_function_step(candidate_value)])
                    else:
                        to_append.append(candidate_value)
                    # Found match in this sublist, continue to the next sublist
                    continue

            # If we reach here, no match was found in the current sublist
            found_in_all = False
            break # Stop checking other sublists for this main_key

        # Only add if suitable values were found in ALL sublists
        if found_in_all: # Implicitly checks len(to_append) == sublists_len
            if custom_function_total:
                # Pass the list of potentially step-transformed values
                final_return.append({main_key: [to_append, custom_function_total(to_append)]})
            else:
                final_return.append({main_key: to_append})
    # --- End Main Processing Loop ---

    return final_return

if __name__ == '__main__':

    now = datetime.now()

    for test in [
        # check the sanity check invalidity
        [{'datetime_lists': [{now: 1}],
          'suppress_sanity_check_messages': True}, None],
        [{'datetime_lists': [{now-timedelta(seconds=60): 1}, {now: 2}],
          'suppress_sanity_check_messages': True}, None],
        [{'datetime_lists': [{now-timedelta(seconds=60): 564,
                              now: 1}],
          'suppress_sanity_check_messages': True}, None],
        [{'datetime_lists': [[1,2,3]],
          'suppress_sanity_check_messages': True}, None],
        [{'datetime_lists': [[[1, 2, 3]]],
          'suppress_sanity_check_messages': True}, None],

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