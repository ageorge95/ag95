from decimal import Decimal

def nr_normalisation(nr: Decimal | str | int | float,
                     decimals_overwrite: int = None) -> str:

    def remove_invalid_trailing(data):
        # remove all trailing 0s and dots (.) or commas (,)
        while data.endswith('0') and len(data) > 1 and (',' in data or '.' in data):
            data = data[:-1]
        if data.endswith('.') or data.endswith(','):
            data = data[:-1]
        return data

    # convert the number to string for processing
    if not isinstance(nr, str):
        nr = str(nr)

    nr = remove_invalid_trailing(nr)

    # figure out the number of decimals
    if '.' not in nr and ',' not in nr:
        nr_decimal_places = 0
    elif '.' in nr and ',' not in nr:
        nr_decimal_places = len(nr.split('.')[1])
    elif ',' in nr and '.' not in nr:
        nr_decimal_places = len(nr.split(',')[1])
    else:
        print('Invalid number provided !')
        return None

    # truncate the decimals if requested
    if nr_decimal_places: # but only if there are decimals

        if '.' in nr:
            nr, decimals = nr.split('.')
            separator = '.'
        elif ',' in nr:
            nr, decimals = nr.split(',')
            separator = ','

        decimals = decimals[:decimals_overwrite]

        nr = nr+separator+decimals

    nr = remove_invalid_trailing(nr)

    return nr

if __name__ == '__main__':

    for test in [
        [[34.2345, 2], '34.23'],
        [[34.2, 1], '34.2'],
        [[34, 1], '34'], [[34, 5], '34'],
        [[34.0, 1], '34'], [[34.0, 5], '34'],
        [[34.2345, 0], '34'], [[43234.23231450000, 0], '43234'],
        [[34.5345, 0], '34'], [[43234.73231450000, 0], '43234'],
        [[Decimal('34'), 1], '34'], [[Decimal('34'), 5], '34'],
        [[Decimal('34.0'), 1], '34'], [[Decimal('34.0'), 5], '34'],
        [[Decimal('34.2345'), 0], '34'], [[Decimal('43234.23231450000'), 0], '43234'],

        [[1.0], '1'], [['1.0'], '1'], [['-1.0'], '-1'],
        [[34.2345], '34.2345'], [[43234.23231450000], '43234.2323145'],
        [[Decimal('34.2345')], '34.2345'], [[Decimal('43234.23231450000')], '43234.2323145'],

        [['34.2345', 2], '34.23'],
        [['34.2', 1], '34.2'],
        [['34', 1], '34'], [[34, 5], '34'],
        [['34.0', 1], '34'], [[34.0, 5], '34'],
        [['34.2345', 0], '34'], [['43234.23231450000', 0], '43234'],
        [['34.5345', 0], '34'], [['43234.73231450000', 0], '43234'],

        [['34,2345', 2], '34,23'],
        [['34,2', 1], '34,2'],
        [['34,', 1], '34'], [[34, 5], '34'],
        [['34,0', 1], '34'], [[34.0, 5], '34'],
        [['34,2345', 0], '34'], [['43234,23231450000', 0], '43234'],
        [['34,5345', 0], '34'], [['43234,73231450000', 0], '43234'],

        [['34,2345.7', 2], None],
        [['34,.2', 1], None],
    ]:
        result = nr_normalisation(*test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {[type(_) for _ in test[0]], test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')