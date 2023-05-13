from decimal import Decimal
# direct and as-a-package execution
try:
    from .nr_normalisation import nr_normalisation
except:
    from nr_normalisation import nr_normalisation

def round_up_closer(nr: Decimal | str | int | float,
                    max_decimals: int) -> str:
    nr = Decimal(str(nr))
    nr_to_add = Decimal("1") / (Decimal("10") ** max_decimals)
    nr_final = (nr + nr_to_add).normalize()
    return nr_normalisation(nr_final,
                            max_decimals)

def round_down_closer(nr: Decimal | str | int | float,
                      max_decimals: int) -> str:
    nr = Decimal(str(nr))
    nr_to_substract = Decimal("1") / (Decimal("10") ** max_decimals)
    nr_final = (nr - nr_to_substract).normalize()
    return nr_normalisation(nr_final,
                            max_decimals)

if __name__ == '__main__':

    for test in [
        [[34.2345, 4], '34.2346'], [[34.0000, 4], '34.0001'],
        [[34.2345, 2], '34.24'], [[34.0000, 2], '34.01'],
    ]:
        result = round_up_closer(*test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {[type(_) for _ in test[0]], test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    for test in [
        [[34.2345, 4], '34.2344'], [[34.0000, 4], '33.9999'],
        [[34.2345, 2], '34.22'], [[34.0000, 2], '33.99'],
    ]:
        result = round_down_closer(*test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {[type(_) for _ in test[0]], test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')