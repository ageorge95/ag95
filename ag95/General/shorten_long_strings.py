from typing import AnyStr

def shorten_long_str(string: AnyStr,
                     separator: AnyStr = '...',
                     cut_length: int = 50):
    if len(string) > cut_length:
        to_cut = int(cut_length/2)
        return f"{string[:to_cut]}{separator}{string[-to_cut:]}"
    else:
        return string

if __name__ == '__main__':
    for test in [
        [['my_long_string'], 'my_long_string'],
        [['my_long_string', '...', 4], 'my...ng'],
        [['my_long_string', '<some_random_txt>', 4], 'my<some_random_txt>ng'],
        [['some very long string that I want to cut in half if it exceeds 20 characters', '...', 35], 'some very long st...eds 20 characters']
    ]:
        result = shorten_long_str(*test[0])
        assert result == test[1] ,\
            f"invalid function return for" \
            f"\n\tinput: {[type(_) for _ in test[0]], test[0]}" \
            f"\n\toutput: {result}" \
            f"\n\texpected: {test[1]}"

    print('All tests are PASSED !')