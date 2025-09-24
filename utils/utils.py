import random
import string


def generate_account_status_name():
    length = random.randint(5, 8)
    name = "".join(random.choices(string.ascii_lowercase, k=length))
    return (
        name.capitalize()
    )  # Capitalize the first letter for a more name-like appearance
