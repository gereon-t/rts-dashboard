import logging
import os

import dash_bootstrap_components as dbc
import dotenv
import networkscan
from dash import ALL, MATCH, Input, Output, State, dcc, html

from app import api, app, models
from app.callbacks.input_validators import validate_ip_address, validate_port
from app.components import ids
from app.components.device import render_device
from app.utils import (
    DeviceNotFound,
    get_button_index,
    get_current_dropdown_options,
    get_device_from_storage,
)


def render_device_list(device_storage: dict[str, dict]) -> list[html.Div]:
    """
    This function renders the device list from the device storage.

    Args:
        device_storage (list[dict]): The current device storage

    Returns:
        list[html.Div]: The device list
    """
    return dcc.Loading(
        id=ids.LOADING,
        children=dbc.ListGroup(
            children=[
                render_device(models.Device(**device))
                for device in device_storage.values()
            ],
            id=ids.DEVICE_LIST,
        ),
    )


@app.callback(
    Output({"type": "device-status-icon", "device_id": MATCH}, "src"),
    Input({"type": "device-test", "device_id": ALL}, "n_clicks"),
    Input({"type": "device-test", "device_id": ALL}, "id"),
    State(ids.DEVICE_STORAGE, "data"),
)
def test_device_connection(
    n_clicks: list[int | None],
    trigger_info: list[dict],
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the "Test" button for a device.

    It will update the status icon for the device to either a green or red light
    depending on whether the device is reachable or not.

    Args:
        n_clicks (list[int | None]): The number of times the button has been clicked
        trigger_info (list[dict]): The information about the button that was clicked
        device_storage (list[dict]): The current device storage

    Returns:
        str: The URL of the icon to display
    """
    if not any(n_clicks):
        return app.get_asset_url("status-unknown.svg")

    button_index = get_button_index(n_clicks)
    device_id = trigger_info[button_index]["device_id"]

    try:
        device = get_device_from_storage(device_id, device_storage)
    except DeviceNotFound:
        return app.get_asset_url("status-error.svg")

    connection_status = api.validate_device_connection(device)
    if connection_status:
        return app.get_asset_url("status-success.svg")
    else:
        return app.get_asset_url("status-error.svg")


@app.callback(
    Output(ids.DEVICE_STORAGE, "data", allow_duplicate=True),
    Input({"type": "device-remove", "device_id": ALL}, "n_clicks"),
    Input({"type": "device-remove", "device_id": ALL}, "id"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def remove_device(
    n_clicks: list[int | None],
    trigger_info: list[dict],
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the "Remove" button for a device.

    It will remove the device from the device storage.

    Args:
        n_clicks (list[int]): The number of times the button has been clicked
        trigger_info (list[dict]): The information about the button that was clicked
        device_storage (list[dict]): The current device storage

    Returns:
        list[dict]: The updated device storage
    """
    if not any(n_clicks):
        return device_storage

    button_index = get_button_index(n_clicks)
    device_id = trigger_info[button_index]["device_id"]
    del device_storage[str(device_id)]

    return device_storage


@app.callback(
    Output(ids.DEVICE_LIST, "children"),
    Output(ids.DEVICE_DROPDOWN, "options"),
    Input(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def update_device_list(device_storage: dict[str, dict]):
    """
    This callback is triggered when the device storage is updated.

    It will update the device list and the device dropdown options
    in the RTS modal.

    Args:
        device_storage (list[dict]): The current device storage

    Returns:
        list[html.Div]: The updated device list
        list[dict]: The updated device dropdown options
    """
    device_list = render_device_list(device_storage)
    dropdown_options = get_current_dropdown_options(device_storage)

    return device_list, dropdown_options


@app.callback(
    Output(ids.DEVICE_MODAL, "is_open", allow_duplicate=True),
    [
        Input(ids.OPEN_DEVICE_MODAL_BUTTON, "n_clicks"),
        Input(ids.CLOSE_DEVICE_MODAL_BUTTON, "n_clicks"),
    ],
    [State(ids.DEVICE_MODAL, "is_open")],
    prevent_initial_call=True,
)
def toggle_modal(n1, n2, is_open):
    """
    This callback is triggered when the user clicks on the "Add Logging Device" button or
    the "Close" button of the device modal.

    It will open or close the device modal.

    Args:
        n1 (int): The number of times the "Add Logging Device" button has been clicked
        n2 (int): The number of times the "Close" button has been clicked
        is_open (bool): Whether the device modal is open

    Returns:
        bool: Whether the device modal is open
    """
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output(ids.DEVICE_STORAGE, "data", allow_duplicate=True),
    Output(ids.DEVICE_MODAL, "is_open", allow_duplicate=True),
    Output(ids.INVALID_DEVICE_INPUT_ALERT, "is_open", allow_duplicate=True),
    Input(ids.CREATE_DEVICE_BUTTON, "n_clicks"),
    State(ids.DEVICE_NAME_INPUT, "value"),
    State(ids.DEVICE_IP_INPUT, "value"),
    State(ids.DEVICE_PORT_INPUT, "value"),
    State(ids.DEVICE_MODAL, "is_open"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def device_modal_actions(
    n_clicks_create_device: int,
    device_name: str,
    device_ip: str,
    device_port: int,
    modal_is_open: bool,
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the "Create" button
    in the device modal.

    It will create a new device and add it to the device storage.

    Args:
        n_clicks_create_device (int): The number of times the "Create" button has been clicked
        device_name (str): The name of the device
        device_ip (str): The IP address of the device
        device_port (int): The port of the device
        modal_is_open (bool): Whether the device modal is open

    Returns:
        list[dict]: The updated device storage
        bool: Whether the device modal is open
        bool: Whether the device input is invalid
    """
    if (
        n_clicks_create_device
        and device_name
        and validate_ip_address(device_ip)
        and validate_port(device_port)
    ):
        device = models.Device(
            id=len(device_storage),
            ip=device_ip,
            port=device_port,
            name=device_name,
        )
        device_storage[str(device.id)] = device.model_dump()
        return device_storage, not modal_is_open, False

    return device_storage, modal_is_open, True


@app.callback(
    Output(ids.DEVICE_STORAGE, "data", allow_duplicate=True),
    Input(ids.SCAN_DEVICES_BUTTON, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def scan_for_devices(_: int, device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Scan" button.

    It will scan the network for devices and add them to the device storage.

    Args:
        _: The number of times the button has been clicked
        device_storage (list[dict]): The current device storage

    Returns:
        list[dict]: The updated device storage
    """
    dotenv.load_dotenv()

    network = os.getenv("NETWORK", "192.168.0.0/24")
    port = int(os.getenv("PORT", "8000"))
    print(f"Scanning network {network} on port {port}")
    logging.info("Scanning network %s on port %s", network, port)
    scan = networkscan.Networkscan(network)
    # This will cause problems if the scan takes longer than 30s"
    scan.run()

    for host in scan.list_of_hosts_found:
        device = models.Device(id=len(device_storage), ip=host, port=port, name=host)

        if not api.validate_device_connection(device):
            continue

        device_storage[str(device.id)] = device.model_dump()

    return device_storage
