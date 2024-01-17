import ipaddress
from typing import Tuple

from dash import Input, Output

from app import app
from app.components import ids


def validate_ip_address(ip_string) -> bool:
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False


def validate_port(port_number: int) -> bool:
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
    if not number:
        return False, False

    valid = validate_port(number)
    return valid, not valid
