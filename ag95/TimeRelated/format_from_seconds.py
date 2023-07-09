def format_from_seconds(seconds: [int, float],
                        granularity: int = 2):

    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

if __name__ == '__main__':

    for test in [
        [[60, 2], '1 minute'],
        [[60*2, 2], '2 minutes'],
        [[60*60, 2], '1 hour'],
        [[60*60*2, 2], '2 hours'],
        [[60*60*2+60, 2], '2 hours, 1 minute']
    ]:
        result = format_from_seconds(*test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {[type(_) for _ in test[0]], test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')