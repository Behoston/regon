import dataclasses
import typing


@dataclasses.dataclass(slots=True, frozen=True)
class REGON:
    # Data provided
    raw_number: str
    # Parsed
    district_number: str
    serial_number: str
    check_digit: str
    normalized_number: str
    # Properties
    is_valid: bool
    is_old: bool
    multiple_districts: bool

    def __str__(self):
        return self.normalized_number

    def __repr__(self):
        return f'REGON({self.normalized_number})'


def parse(regon_number: typing.Union[str, int], raise_on_invalid: bool = True) -> REGON:
    regon_str: str
    if isinstance(regon_number, int):
        regon_str = str(regon_number)
    elif isinstance(regon_number, str):
        regon_str = regon_number
    else:
        raise ValueError("Regon number must be string or integer!")
    if regon_str.isnumeric() is False:
        raise ValueError("Regon number contains illegal characters!")
    chars = len(regon_str)
    if chars not in {7, 9, 14}:
        raise ValueError("Regon should have 7, 9 or 14 chars length!")

    district_number = regon_str[:2] if chars != 7 else '00'
    serial_number = regon_str[2:-1] if chars != 7 else regon_str[:-1]
    check_digit = regon_str[-1]
    obj = REGON(
        raw_number=regon_str,
        district_number=district_number,
        serial_number=serial_number,
        check_digit=check_digit,
        normalized_number=f'{district_number}{serial_number}{check_digit}',
        is_old=district_number == '00',
        is_valid=is_valid(f'{district_number}{serial_number}', check_digit, chars),
        multiple_districts=chars == 14,
    )
    if raise_on_invalid and obj.is_valid is False:
        raise ValueError("Regon is invalid!")
    return obj


def is_valid(number: str, check_digit: str, chars: int) -> bool:
    weights: typing.Iterable[int]
    if chars == 14:
        weights = (2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8)
    else:
        weights = (8, 9, 2, 3, 4, 5, 6, 7)
    valid_check_digit = sum(map(lambda w, n: w * int(n), weights, number)) % 11
    valid_check_digit = valid_check_digit if valid_check_digit != 10 else 0
    return str(valid_check_digit) == check_digit
