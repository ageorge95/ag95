from typing import AnyStr

def shorten_long_str(string: AnyStr,
                     separator: AnyStr = '...',
                     cut_length: int = 50):
    if len(string) > cut_length:
        half = int(len(string)/2)
        return f"{string[:min(half,int(cut_length/2))]}{separator}{string[-min(half,int(cut_length/2)):]}"
    else:
        return string

if __name__ == '__main__':
    for test in [
        [['my_long_string'], 'my_long_string'],
        [['my_long_string', '...', 4], 'my_l...ring'],
        [['my_long_string', '<some_random_txt>', 4], 'my_l<some_random_txt>ring']
    ]:
        result = shorten_long_str(*test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {[type(_) for _ in test[0]], test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')