from typing import Literal

def red_green_from_range_value(value,
                               min_value,
                               max_value,
                               return_as: Literal["tuple", "hex"] = "tuple"):
    # Function that returns an RGB color (between red and green)
    # based on a specified value and a minimum and maximum
    # Ensure value is within the range [min_value, max_value]
    value = max(min(value, max_value), min_value)

    # Calculate the ratio of the value within the range
    ratio = (value - min_value) / (max_value - min_value)

    # Interpolate between green (0, 255, 0) and red (255, 0, 0)
    red = int(ratio * 255)  # Red increases as the value increases
    green = int((1 - ratio) * 255)  # Green decreases as the value increases

    # return the RGB value
    if return_as == 'tuple':
        return (red, green, 0)
    elif return_as == 'hex':
        return '#{:02X}{:02X}{:02X}'.format(*(red, green, 0))
    else:
        return None

if __name__ == '__main__':
    r, g, b = red_green_from_range_value(-10, 0, 100)
    print(f"\033[38;2;{r};{g};{b}mThis text should be green (value lower than minimum)!\033[0m")

    r, g, b = red_green_from_range_value(0, 0, 100)
    print(f"\033[38;2;{r};{g};{b}mThis text should be green!\033[0m")

    r, g, b = red_green_from_range_value(25, 0, 100)
    print(f"\033[38;2;{r};{g};{b}mThis text should be halfway between red and green, closer to green!\033[0m")

    r, g, b = red_green_from_range_value(50, 0, 100)
    print(f"\033[38;2;{r};{g};{b}mThis text should be halfway between red and green!\033[0m")

    r, g, b = red_green_from_range_value(75, 0, 100)
    print(f"\033[38;2;{r};{g};{b}mThis text should be halfway between red and green, closer to red!\033[0m")

    r, g, b = red_green_from_range_value(100, 0, 100)
    print(f"\033[38;2;{r};{g};{b}mThis text should be red!\033[0m")

    r, g, b = red_green_from_range_value(110, 0, 100)
    print(f"\033[38;2;{r};{g};{b}mThis text should be red (value higher than maximum)!\033[0m")

    print('Check that the text color above is like the text description.')