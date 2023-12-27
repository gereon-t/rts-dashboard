import logging

from dash import ALL, MATCH, Input, Output, State, html

from app import api, app, device_cache, models
from app.components import ids
from app.components.rts import render_rts

logger = logging.getLogger("root")


def get_current_rts_list():
    rts_children = []

    for device in device_cache.get_all():
        device_rts = api.get_rts(device)

        for rts in device_rts:
            rts_children.append(render_rts(device=device, rts=rts))

    return rts_children


@app.callback(
    Output(
        {"type": "rts-serial-status-icon", "rts_id": MATCH, "device_id": MATCH}, "src"
    ),
    Input({"type": "rts-test", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "rts-test", "rts_id": MATCH, "device_id": MATCH}, "id"),
    prevent_initial_call=True,
)
def test_rts_connection(_: int, trigger_info: dict):
    logger.info(
        "Testing RTS %i of device %i", trigger_info["rts_id"], trigger_info["device_id"]
    )
    device_id = trigger_info["device_id"]
    rts_id = trigger_info["rts_id"]
    db_device = device_cache.get(device_id)

    if db_device is None:
        logger.error("Failed to get device with id: %s", device_id)
        return app.get_asset_url("status-error.svg")

    device = models.Device(**db_device.__dict__)
    connection_status = api.validate_rts_connection(device=device, rts_id=rts_id)
    if connection_status:
        api.ping_rts(device=device, rts_id=rts_id)
        return app.get_asset_url("status-success.svg")
    else:
        return app.get_asset_url("status-error.svg")


@app.callback(
    Output(
        {"type": "rts-tracking-status-icon", "rts_id": MATCH, "device_id": MATCH},
        "src",
        allow_duplicate=True,
    ),
    Input({"type": "rts-start", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "rts-start", "rts_id": MATCH, "device_id": MATCH}, "id"),
    prevent_initial_call=True,
)
def start_tracking(_: int, trigger_info: dict):
    device_id = trigger_info["device_id"]
    rts_id = trigger_info["rts_id"]
    device = device_cache.get(device_id)
    api.start_tracking(device=device, rts_id=rts_id)
    return app.get_asset_url("status-success.svg")


@app.callback(
    Output(
        {"type": "rts-tracking-status-icon", "rts_id": MATCH, "device_id": MATCH},
        "src",
        allow_duplicate=True,
    ),
    Input({"type": "rts-dummy", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "rts-dummy", "rts_id": MATCH, "device_id": MATCH}, "id"),
    prevent_initial_call=True,
)
def start_dummy_tracking(_: int, trigger_info: dict):
    device_id = trigger_info["device_id"]
    rts_id = trigger_info["rts_id"]
    device = device_cache.get(device_id)
    api.start_dummy_tracking(device=device, rts_id=rts_id)
    return app.get_asset_url("status-success.svg")


@app.callback(
    Output(
        {"type": "rts-tracking-status-icon", "rts_id": MATCH, "device_id": MATCH},
        "src",
        allow_duplicate=True,
    ),
    Input({"type": "rts-stop", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "rts-stop", "rts_id": MATCH, "device_id": MATCH}, "id"),
    prevent_initial_call=True,
)
def stop_tracking(_: int, trigger_info: dict):
    device_id = trigger_info["device_id"]
    rts_id = trigger_info["rts_id"]
    device = device_cache.get(device_id)
    api.stop_tracking(device=device, rts_id=rts_id)
    return app.get_asset_url("status-unknown.svg")


@app.callback(
    Output({"type": "dummy-output", "rts_id": MATCH, "device_id": MATCH}, "children"),
    Input({"type": "rts-change-face", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "rts-change-face", "rts_id": MATCH, "device_id": MATCH}, "id"),
    prevent_initial_call=True,
)
def change_face(_: int, trigger_info: dict):
    device_id = trigger_info["device_id"]
    rts_id = trigger_info["rts_id"]
    device = device_cache.get(device_id)
    api.change_face(device=device, rts_id=rts_id)
    return ""


@app.callback(
    Output(ids.RTS_LIST, "children", allow_duplicate=True),
    Input({"type": "rts-remove", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    Input({"type": "rts-remove", "rts_id": ALL, "device_id": ALL}, "id"),
    prevent_initial_call=True,
)
def remove_rts(n_clicks: int, trigger_info: dict):
    if any(n_clicks):
        button_index = next((i for i in range(len(n_clicks)) if n_clicks[i] is not None), None)
        device_id = trigger_info[button_index]["device_id"]
        rts_id = trigger_info[button_index]["rts_id"]
        device = device_cache.get(device_id)
        api.delete_rts(device=device, rts_id=rts_id)
    return get_current_rts_list()


@app.callback(
    Output(
        {"type": "rts-tracking-status-icon", "rts_id": MATCH, "device_id": MATCH}, "src"
    ),
    Output(
        {"type": "rts-position-count", "rts_id": MATCH, "device_id": MATCH}, "children"
    ),
    Input(
        {"type": "rts-tracking-status-interval", "rts_id": MATCH, "device_id": MATCH},
        "n_intervals",
    ),
    Input(
        {"type": "rts-tracking-status-interval", "rts_id": MATCH, "device_id": MATCH},
        "id",
    ),
    prevent_initial_call=True,
)
def update_tracking_status(_: int, trigger_info: dict):
    device_id = trigger_info["device_id"]
    rts_id = trigger_info["rts_id"]
    db_device = device_cache.get(device_id)

    if db_device is None:
        logger.error("Failed to get device with id: %s", device_id)
        return app.get_asset_url("status-error.svg"), "Recorded Positions: 0"

    device = models.Device(**db_device.__dict__)
    response = api.get_tracking_status(device=device, rts_id=rts_id)

    tracking_status = response["active"]
    num_positions = f"Recorded Positions: {response['positions']}"

    if tracking_status:
        return app.get_asset_url("status-success.svg"), num_positions

    return app.get_asset_url("status-error.svg"), num_positions


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
    State(ids.RTS_LIST, "children"),
    State(ids.RTS_MODAL, "is_open"),
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
    current_rts: list[html.Div],
    modal_is_open: bool,
):
    if (
        n_clicks_create_rts
        and rts_name
        and rts_port
        and rts_baudrate
        and rts_parity
        and rts_stopbits
        and rts_bytesize
        and rts_timeout
    ):
        db_device = device_cache.get(device_id)

        if db_device is None:
            logger.error("Failed to get device with id: %s", device_id)
            return (
                current_rts,
                modal_is_open,
                f"Failed to get device with id: {device_id} from database.",
                True,
            )

        device = models.Device(**db_device.__dict__)

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
            return current_rts, modal_is_open, "API request to device failed.", True

        current_rts.append(render_rts(rts=added_rts, device=db_device))
        return current_rts, not modal_is_open, "", False

    return current_rts, modal_is_open, "Inputs incomplete.", True


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input(ids.START_ALL_BUTTON, "n_clicks"),
    prevent_initial_call=True,
)
def start_all(_: int):
    devices = device_cache.get_all()
    for device in devices:
        device = models.Device(**device.__dict__)

        rts_list = api.get_rts(device)
        for rts in rts_list:
            api.start_tracking(device=device, rts_id=rts.id)
            logger.info("Started tracking for RTS %i", rts.id)

    return ""


@app.callback(
    Output(ids.DUMMY_OUTPUT, "children", allow_duplicate=True),
    Input(ids.STOP_ALL_BUTTON, "n_clicks"),
    prevent_initial_call=True,
)
def stop_all(_: int):
    devices = device_cache.get_all()
    for device in devices:
        device = models.Device(**device.__dict__)

        rts_list = api.get_rts(device)
        for rts in rts_list:
            api.stop_tracking(device=device, rts_id=rts.id)
            logger.info("Stopped tracking for RTS %i", rts.id)

    return ""
