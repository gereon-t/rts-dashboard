import logging
import time
from typing import Callable

from dash import ALL, MATCH, Input, Output, State, ctx

from app import api, app, models
from app.components import ids
from app.components.rts import render_rts
from app.utils import DeviceNotFound, get_device_from_storage

logger = logging.getLogger("root")

STATUS_ICONS = {
    True: app.get_asset_url("status-success.svg"),
    False: app.get_asset_url("status-error.svg"),
}


def handle_api_request(
    api_func: Callable[[models.Device, int], bool],
    trigger_id: dict,
    device_storage: dict[str, dict],
) -> None:
    """
    Helper function to handle API requests.

    Args:
        api_func (Callable[[models.Device, int], bool]): The API function to call
        trigger_id (dict): The information about the button that was clicked
        device_storage (dict[str, dict]): The current device storage

    """
    try:
        device, rts_id = get_device_and_rts_id(
            trigger_id=trigger_id, device_storage=device_storage
        )
        api_success = api_func(device, rts_id)
    except DeviceNotFound:
        logger.error("Failed to get device")

    if not api_success:
        logger.error("API request to device failed.")

    return


def get_device_and_rts_id(
    trigger_id: dict, device_storage: dict[str, dict]
) -> tuple[models.Device, int]:
    """
    This function returns the device and RTS ID of the button that was clicked.

    Raises:
        DeviceNotFound: If the device with the given ID is not in the device storage

    Args:
        n_clicks (int): The number of times the button has been clicked
        trigger_id (dict): The information about the button that was clicked

    Returns:
        tuple[models.Device, int]: The device and RTS ID of the button that was clicked
    """
    device_id = trigger_id["device_id"]
    rts_id = trigger_id["rts_id"]

    device = get_device_from_storage(device_id=device_id, device_storage=device_storage)
    return device, rts_id


def render_rts_list(device_storage: dict[str, dict]):
    """
    This function renders the RTS list from the device storage.

    Args:
        device_storage (dict[str, dict]): The current device storage

    Returns:
        list[html.Div]: The RTS list
    """
    rts_children = []

    for device_dict in device_storage.values():
        device = models.Device(**device_dict)
        device_rts = api.get_rts(device)

        for rts in device_rts:
            rts_children.append(render_rts(device=device, rts=rts))

    return rts_children


@app.callback(
    Output(ids.RTS_LIST, "children", allow_duplicate=True),
    Input(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def update_rts_list(device_storage: dict[str, dict]):
    return render_rts_list(device_storage)


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input({"type": "rts-test", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def test_rts_connection(n_clicks: list[int], device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Test" button for a RTS.

    It will test the connection to the RTS and update the status icon.

    Args:
        n_clicks (list[int]): The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage
    """
    if not any(n_clicks):
        return

    handle_api_request(
        api_func=api.validate_rts_connection,
        trigger_id=ctx.triggered_id,
        device_storage=device_storage,
    )


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input({"type": "rts-start", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def start_tracking(n_clicks: list[int], device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Start" button for a RTS.

    It will start tracking for the RTS by sending an API request to the device.

    Args:
        n_clicks (list[int]): The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage
    """
    if not any(n_clicks):
        return

    handle_api_request(
        api_func=api.start_tracking,
        trigger_id=ctx.triggered_id,
        device_storage=device_storage,
    )


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input({"type": "rts-dummy", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def start_dummy_tracking(n_clicks: list[int], device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Start Dummy Tracking" button for a RTS.

    It will start fake tracking for the RTS by sending an API request to the device.

    Args:
        n_clicks (list[int]): The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage
    """
    if not any(n_clicks):
        return

    handle_api_request(
        api_func=api.start_dummy_tracking,
        trigger_id=ctx.triggered_id,
        device_storage=device_storage,
    )


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input({"type": "rts-stop", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def stop_tracking(n_clicks: list[int], device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Stop" button for a RTS.

    It will stop tracking for the RTS by sending an API request to the device.

    Args:
        n_clicks (list[int]): The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage
    """
    if not any(n_clicks):
        return

    handle_api_request(
        api_func=api.stop_tracking,
        trigger_id=ctx.triggered_id,
        device_storage=device_storage,
    )


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input({"type": "rts-change-face", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def change_face(n_clicks: list[int], device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Change Face" button for a RTS.

    It will change the face of the RTS by sending an API request to the device.

    Args:
        n_clicks (list[int]): The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage
    """
    if not any(n_clicks):
        return

    handle_api_request(
        api_func=api.change_face,
        trigger_id=ctx.triggered_id,
        device_storage=device_storage,
    )


@app.callback(
    Output(ids.RTS_LIST, "children", allow_duplicate=True),
    Input({"type": "rts-remove", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def remove_rts(n_clicks: list[int], device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Remove" button for a RTS.

    It will remove the RTS from the device by sending an API request to the device.

    Args:
        n_clicks (list[int]): The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage
    """
    if not any(n_clicks):
        return render_rts_list(device_storage)

    handle_api_request(
        api_func=api.delete_rts,
        trigger_id=ctx.triggered_id,
        device_storage=device_storage,
    )
    return render_rts_list(device_storage)


@app.callback(
    Output(
        {"type": "rts-serial-status-icon", "rts_id": MATCH, "device_id": MATCH}, "src"
    ),
    Output(
        {"type": "rts-tracking-status-icon", "rts_id": MATCH, "device_id": MATCH}, "src"
    ),
    Output(
        {"type": "rts-position-count", "rts_id": MATCH, "device_id": MATCH}, "children"
    ),
    Output(
        {"type": "rts-position-storage", "rts_id": MATCH, "device_id": MATCH}, "data"
    ),
    Input(
        {"type": "rts-tracking-status-interval", "rts_id": MATCH, "device_id": MATCH},
        "n_intervals",
    ),
    Input(
        {"type": "rts-tracking-status-interval", "rts_id": MATCH, "device_id": MATCH},
        "id",
    ),
    State(
        {"type": "rts-position-storage", "rts_id": MATCH, "device_id": MATCH}, "data"
    ),
    State(ids.DEVICE_STORAGE, "data"),
)
def update_tracking_status(
    _: int, trigger_info: dict, stored_position: dict, device_storage: dict[str, dict]
):
    """
    This callback is triggered when the tracking status interval fires. It will update
    the tracking status of the RTS every second by sending an API request to the device.

    Args:
        _: The number of times the interval has fired
        trigger_info (dict): The information about the button that was clicked
        stored_position (dict): The current stored position
        device_storage (dict[str, dict]): The current device storage

    Returns:
        tuple: The status icons for the connection and tracking status, the number of
            recorded positions and the current stored position
    """
    try:
        device, rts_id = get_device_and_rts_id(
            trigger_id=trigger_info, device_storage=device_storage
        )
    except DeviceNotFound:
        logger.error("Failed to get device")
        return (
            app.get_asset_url("status-error.svg"),
            app.get_asset_url("status-error.svg"),
            "0",
            stored_position,
        )

    tracking_response = api.get_tracking_status(device=device, rts_id=rts_id)
    connection_response = api.get_connection_status(device=device, rts_id=rts_id)

    if tracking_response is None or connection_response is None:
        return (
            app.get_asset_url("status-error.svg"),
            app.get_asset_url("status-error.svg"),
            "0",
            stored_position,
        )

    tracking_status = tracking_response["active"]
    connection_status = connection_response["connected"]
    num_positions = tracking_response["positions"]

    if tracking_status:
        position = {
            k: v
            for k, v in tracking_response.items()
            if k in ["pos_x", "pos_y", "pos_z", "device"]
        }
        stored_position = position
        stored_position["timestamp"] = time.time()
    else:
        stored_position = {
            "timestamp": 0,
            "device": "None",
            "pos_x": 0,
            "pos_y": 0,
            "pos_z": 0,
        }

    return (
        STATUS_ICONS[connection_status],
        STATUS_ICONS[tracking_status],
        num_positions,
        stored_position,
    )


@app.callback(
    Output(ids.RTS_POSITION_STORAGE, "data"),
    Input({"type": "rts-position-storage", "rts_id": ALL, "device_id": ALL}, "data"),
    prevent_initial_call=True,
)
def update_target_position(stored_positions: list[dict]):
    if not stored_positions:
        stored_positions = [
            {"timestamp": 0, "pos_x": 0, "pos_y": 0, "pos_z": 0, "device": "None"}
        ]

    newest_position = max(stored_positions, key=lambda x: x["timestamp"])

    return newest_position


@app.callback(
    Output(ids.RTS_MODAL, "is_open", allow_duplicate=True),
    [
        Input(ids.OPEN_RTS_MODAL_BUTTON, "n_clicks"),
        Input(ids.CLOSE_RTS_MODAL_BUTTON, "n_clicks"),
    ],
    [State(ids.RTS_MODAL, "is_open")],
    prevent_initial_call=True,
)
def toggle_modal(n1, n2, is_open):
    """
    This callback is triggered when the user clicks on the "Add RTS" button.

    It will open or close the RTS modal.

    Args:
        n1 (int): The number of times the "Add RTS" button has been clicked
        n2 (int): The number of times the "Close" button has been clicked
        is_open (bool): Whether the RTS modal is open

    Returns:
        bool: Whether the RTS modal is open
    """
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output(ids.RTS_LIST, "children", allow_duplicate=True),
    Output(ids.RTS_MODAL, "is_open", allow_duplicate=True),
    Output(ids.INVALID_RTS_INPUT_ALERT, "children"),
    Output(ids.INVALID_RTS_INPUT_ALERT, "is_open"),
    Input(ids.CREATE_RTS_BUTTON, "n_clicks"),
    State(ids.DEVICE_DROPDOWN, "value"),
    State(ids.RTS_NAME_INPUT, "value"),
    State(ids.RTS_PORT_INPUT, "value"),
    State(ids.RTS_BAUDRATE_INPUT, "value"),
    State(ids.RTS_PARITY_INPUT, "value"),
    State(ids.RTS_STOPBITS_INPUT, "value"),
    State(ids.RTS_BYTESIZE_INPUT, "value"),
    State(ids.RTS_TIMEOUT_INPUT, "value"),
    State(ids.RTS_MODAL, "is_open"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def rts_modal_actions(
    n_clicks_create_rts: int,
    device_id: int,
    rts_name: str,
    rts_port: str,
    rts_baudrate: int,
    rts_parity: str,
    rts_stopbits: int,
    rts_bytesize: int,
    rts_timeout: int,
    modal_is_open: bool,
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the "Add" button of the RTS modal.

    It will add the RTS to the device by sending an API request to the device.

    Args:
        n_clicks_create_rts (int): The number of times the "Add" button has been clicked
        device_id (int): The ID of the device
        rts_name (str): The name of the RTS
        rts_port (str): The port of the RTS
        rts_baudrate (int): The baudrate of the RTS
        rts_parity (str): The parity of the RTS
        rts_stopbits (int): The stopbits of the RTS
        rts_bytesize (int): The bytesize of the RTS
        rts_timeout (int): The timeout of the RTS
        modal_is_open (bool): Whether the RTS modal is open
        device_storage (dict[str, dict]): The current device storage

    Returns:
        bool: Whether the RTS modal is open
        str: The alert message
        bool: Whether the alert is open
    """
    if not (
        n_clicks_create_rts
        and rts_name
        and rts_port
        and rts_baudrate
        and rts_parity
        and rts_stopbits
        and rts_bytesize
        and rts_timeout
    ):
        return (
            render_rts_list(device_storage),
            modal_is_open,
            "Inputs incomplete.",
            True,
        )

    db_device = device_storage.get(str(device_id))

    if db_device is None:
        return render_rts_list(device_storage), modal_is_open, "Device not found.", True

    device = models.Device(**db_device)

    rts_api = models.RTS_APICreate(
        name=rts_name,
        port=rts_port,
        baudrate=rts_baudrate,
        parity=rts_parity,
        stopbits=rts_stopbits,
        bytesize=rts_bytesize,
        timeout=rts_timeout,
    )

    added_rts = api.add_rts(device=device, rts=rts_api)

    if added_rts is None:
        return (
            render_rts_list(device_storage),
            modal_is_open,
            "API request to device failed.",
            True,
        )

    return render_rts_list(device_storage), not modal_is_open, "", False


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input(ids.START_ALL_BUTTON, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def start_all(_: int, device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Start All" button.

    It will start tracking for all RTS by sending an API request to the device.

    Args:
        _: The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage

    Returns:
        str: An empty string, to prevent the callback from returning None
    """
    for device_dict in device_storage.values():
        device = models.Device(**device_dict)

        rts_list = api.get_rts(device)
        for rts in rts_list:
            api.start_tracking(device=device, rts_id=rts.id)
            logger.info("Started tracking for RTS %i", rts.id)

    return


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input(ids.STOP_ALL_BUTTON, "n_clicks"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def stop_all(_: int, device_storage: dict[str, dict]):
    """
    This callback is triggered when the user clicks on the "Stop All" button.

    It will stop tracking for all RTS by sending an API request to the device.

    Args:
        _: The number of times the button has been clicked
        device_storage (dict[str, dict]): The current device storage

    Returns:
        str: An empty string, to prevent the callback from returning None
    """
    for device_dict in device_storage.values():
        device = models.Device(**device_dict)

        rts_list = api.get_rts(device)
        for rts in rts_list:
            api.stop_tracking(device=device, rts_id=rts.id)
            logger.info("Stopped tracking for RTS %i", rts.id)

    return
