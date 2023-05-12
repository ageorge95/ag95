from decimal import Decimal

def decimals_places(nr: Decimal | str | float | int) -> int:

    nr = str(nr)

    while nr.endswith('0'):
        nr = nr[:-1]

    return abs(Decimal(nr).as_tuple().exponent)

if __name__ == '__main__':

    for test in [
        [1.0, 0], ['1.0', 0], ['1.00', 0],
        [0.0, 0], ['0.0', 0], ['0.00', 0],
        [-1.0, 0], ['-1.0', 0], ['-1.00', 0],
        [1, 0], ['1', 0],
        [5464, 0], ['5464', 0],
        [-1, 0], ['-1', 0],
        [1.1, 1], [1.114, 3], [-4.56, 2],
        ['1.1', 1], ['1.114', 3], ['-4.56', 2],
        [1.10, 1], [1.11400, 3], [-4.56000, 2],
        ['1.10', 1], ['1.11400', 3], ['-4.56000', 2],
        ['.1', 1], ['.1456', 4],
        [Decimal('1.10'), 1], [Decimal('1.11400'), 3], [Decimal('-4.56000'), 2],
        [Decimal('.1'), 1], [Decimal('.1456'), 4]
    ]:
        result = decimals_places(test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {type(test[0]), test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')