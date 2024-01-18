import logging
from dash import Input, Output, State
import networkscan
from app import api, app, models
from app.callbacks.input_validators import validate_ip_network, validate_port
from app.components import ids


@app.callback(
    Output(ids.SCAN_MODAL, "is_open", allow_duplicate=True),
    [
        Input(ids.OPEN_SCAN_MODAL_BUTTON, "n_clicks"),
        Input(ids.CLOSE_SCAN_MODAL_BUTTON, "n_clicks"),
    ],
    [State(ids.SCAN_MODAL, "is_open")],
    prevent_initial_call=True,
)
def toggle_modal(n1, n2, is_open):
    """
    This callback is triggered when the user clicks on the "Scan for Devices" button or
    the "Close" button of the scan modal.

    It will open or close the scan modal.

    Args:
        n1 (int): The number of times the "Scan for Devices" button has been clicked
        n2 (int): The number of times the "Close" button has been clicked
        is_open (bool): Whether the scan modal is open

    Returns:
        bool: Whether the scan modal is open
    """
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output(ids.DEVICE_STORAGE, "data", allow_duplicate=True),
    Output(ids.SCAN_MODAL, "is_open", allow_duplicate=True),
    Output(ids.INVALID_SCAN_INPUT_ALERT, "is_open", allow_duplicate=True),
    Output(ids.SCAN_DEVICE_LOADING, "children", allow_duplicate=True),
    Input(ids.SCAN_DEVICE_BUTTON, "n_clicks"),
    State(ids.NETWORK_INPUT, "value"),
    State(ids.NETWORK_PORT_INPUT, "value"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def scan_for_devices(
    n_clicks: int, network: str, port: int, device_storage: dict[str, dict]
):
    """
    This callback is triggered when the user clicks on the "Scan" button.

    It will scan the network for devices and add them to the device storage.

    Args:
        _: The number of times the button has been clicked
        device_storage (list[dict]): The current device storage

    Returns:
        dict[dict]: The updated device storage
    """
    if not (
        n_clicks and network and validate_ip_network(network) and validate_port(port)
    ):
        return device_storage, True, True, None

    logging.info("Scanning network %s on port %s", network, port)
    scan = networkscan.Networkscan(network)
    # This will cause problems if the scan takes longer than 30s"
    scan.run()

    for host in scan.list_of_hosts_found:
        device = models.Device(id=len(device_storage), ip=host, port=port, name=host)

        if not api.validate_device_connection(device):
            continue

        device_storage[str(device.id)] = device.model_dump()

    return device_storage, False, False, None
