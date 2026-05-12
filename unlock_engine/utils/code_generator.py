import random
import string


def generate_pass_code(prefix="JB26"):

    part_one = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=4
        )
    )

    part_two = ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=4
        )
    )

    return f"{prefix}-{part_one}-{part_two}"


def generate_serial_number():

    return ''.join(
        random.choices(
            string.digits,
            k=12
        )
    )