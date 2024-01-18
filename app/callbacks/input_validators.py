import ipaddress
from typing import Tuple

from dash import Input, Output

from app import app
from app.components import ids


def validate_ip_address(ip_string: str) -> bool:
    """
    Check if the given string is a valid IP address.

    Args:
        ip_string (str): The string to check.

    Returns:
        bool: True if the string is a valid IP address, False otherwise.
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def validate_port(port_number: int) -> bool:
    """
    Check if the given number is a valid port number.

    Args:
        port_number (int): The number to check.

    Returns:
        bool: True if the number is a valid port number, False otherwise.
    """
    if port_number % 1 != 0:
        return False
    return 0 < port_number <= 65535


@app.callback(
    [Output(ids.DEVICE_IP_INPUT, "valid"), Output(ids.DEVICE_IP_INPUT, "invalid")],
    [
        Input(ids.DEVICE_IP_INPUT, "value"),
    ],
)
def update_ip_form(text: str) -> Tuple[bool, bool]:
    """
    This callback is triggered when the input value of the IP address input field changes.

    Args:
        text (str): The value of the IP address input field.

    Returns:
        Tuple[bool, bool]: A tuple of two boolean values. The first value indicates if the
        input is valid, the second value indicates if the input is invalid.
    """
    if not text:
        return False, False

    valid = validate_ip_address(text)
    return valid, not valid


@app.callback(
    [
        Output(ids.DEVICE_PORT_INPUT, "valid"),
        Output(ids.DEVICE_PORT_INPUT, "invalid"),
    ],
    [
        Input(ids.DEVICE_PORT_INPUT, "value"),
    ],
)
def update_port_form(number: int) -> Tuple[bool, bool]:
    """
    This callback is triggered when the input value of the port input field changes.

    Args:
        number (int): The value of the port input field.

    Returns:
        Tuple[bool, bool]: A tuple of two boolean values. The first value indicates if the
        input is valid, the second value indicates if the input is invalid.
    """
    if not number:
        return False, False

    valid = validate_port(number)
    return valid, not valid
