import random

# https://stackoverflow.com/a/1210632/489239


def unique_id():
    seed = random.getrandbits(32)
    while True:
        yield seed
        seed += 1


unique_sequence = unique_id()


def UID(prefix: str = "") -> str:
    """Generator method that returns unique IDs prepended with the given prefix

    Args:
        prefix (str, optional): The ID prefix Defaults to "".

    Returns:
        str: The unique ID, eg (user-da80b519)
    """
    prefix = f"{prefix}-" if prefix else "I"
    return f"{prefix}{hex(next(unique_sequence))[2:]}"
