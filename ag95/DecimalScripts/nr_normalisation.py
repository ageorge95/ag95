from decimal import Decimal

def nr_normalisation(nr: Decimal | str | int | float,
                     decimals_overwrite: int = None) -> str:
    nr = str(nr)

    # first remove any trailing of 0 from the nr
    # nr must first be converted to a Decimal, to correctly display it
    if type(nr) != type(Decimal):
        nr = Decimal(str(nr))

    nr_decimal_places = abs(nr.as_tuple().exponent)
    nr = f'{nr:.{nr_decimal_places if decimals_overwrite is None else decimals_overwrite}f}'

    # now remove all trailing 0s
    while nr.endswith('0') and len(nr) > 1 and (',' in nr or '.' in nr):
        nr = nr[:-1]

    # then convert the number to a decimal
    nr = Decimal(str(nr))

    # and finally return it
    nr_decimal_places = abs(nr.as_tuple().exponent)
    return f'{nr:.{nr_decimal_places}f}'

if __name__ == '__main__':

    for test in [
        [[34.2345, 2], '34.23'],
        [[34.2, 1], '34.2'],
        [[34, 1], '34'], [[34, 5], '34'],
        [[34.0, 1], '34'], [[34.0, 5], '34'],
        [[34.2345, 0], '34'], [[43234.23231450000, 0], '43234'],
        [[Decimal('34'), 1], '34'], [[Decimal('34'), 5], '34'],
        [[Decimal('34.0'), 1], '34'], [[Decimal('34.0'), 5], '34'],
        [[Decimal('34.2345'), 0], '34'], [[Decimal('43234.23231450000'), 0], '43234']
    ]:
        result = nr_normalisation(*test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {[type(_) for _ in test[0]], test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    for test in [
        [1.0, '1'], ['1.0', '1'], ['-1.0', '-1'],
        [34.2345, '34.2345'], [43234.23231450000, '43234.2323145'],
        [Decimal('34.2345'), '34.2345'], [Decimal('43234.23231450000'), '43234.2323145'],
    ]:
        result = nr_normalisation(test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {type(test[0]), test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')