import os
import logging
import dash_bootstrap_components as dbc
import dotenv
import networkscan
from dash import ALL, MATCH, Input, Output, Patch, State, html, dcc
from app import api, app, device_cache, models
from app.callbacks.input_validators import validate_ip_address, validate_port
from app.components import ids
from app.components.device import render_device
from app.callbacks.rts import get_current_rts_list
from app.utils import get_current_dropdown_options


def get_current_device_list() -> list[html.Div]:
    return dcc.Loading(
        id=ids.LOADING,
        children=dbc.ListGroup(
            children=[render_device(device) for device in device_cache.get_all()],
            id=ids.DEVICE_LIST,
        ),
    )


@app.callback(
    Output({"type": "device-status-icon", "device_id": MATCH}, "src"),
    Input({"type": "device-test", "device_id": MATCH}, "n_clicks"),
    Input({"type": "device-test", "device_id": MATCH}, "id"),
    prevent_initial_call=True,
)
def test_device_connection(_: int, trigger_info: dict):
    device_id = trigger_info["device_id"]
    device = device_cache.get(device_id)
    connection_status = api.validate_device_connection(models.Device(**device.__dict__))
    if connection_status:
        return app.get_asset_url("status-success.svg")
    else:
        return app.get_asset_url("status-error.svg")


@app.callback(
    Output(ids.DEVICE_LIST, "children", allow_duplicate=True),
    Input({"type": "device-remove", "device_id": ALL}, "n_clicks"),
    Input({"type": "device-remove", "device_id": ALL}, "id"),
    prevent_initial_call=True,
)
def remove_device(n_clicks: int, trigger_info: dict):
    if any(n_clicks):
        button_index = next((i for i in range(len(n_clicks)) if n_clicks[i] is not None), None)
        device_id = trigger_info[button_index]["device_id"]
        device_cache.delete(device_id)
    return get_current_device_list()


@app.callback(
    Output(ids.DEVICE_DROPDOWN, "options"),
    Output(ids.RTS_LIST, "children", allow_duplicate=True),
    Input(ids.DEVICE_LIST, "children"),
    prevent_initial_call=True,
)
def update_device_list(_: list[html.Div]):
    current_dropdown_options = get_current_dropdown_options()
    current_rts_list_children = get_current_rts_list()

    return current_dropdown_options, current_rts_list_children


@app.callback(
    Output(ids.RTS_LIST, "children", allow_duplicate=True),
    Input({"type": "device-test", "device_id": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def refresh_rts_list(_: int):
    return get_current_rts_list()


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
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output(ids.DEVICE_LIST, "children", allow_duplicate=True),
    Output(ids.DEVICE_MODAL, "is_open", allow_duplicate=True),
    Output(ids.INVALID_DEVICE_INPUT_ALERT, "is_open", allow_duplicate=True),
    Input(ids.CREATE_DEVICE_BUTTON, "n_clicks"),
    State(ids.DEVICE_NAME_INPUT, "value"),
    State(ids.DEVICE_IP_INPUT, "value"),
    State(ids.DEVICE_PORT_INPUT, "value"),
    State(ids.DEVICE_MODAL, "is_open"),
    prevent_initial_call=True,
)
def device_modal_actions(
    n_clicks_create_device: int,
    device_name: str,
    device_ip: str,
    device_port: int,
    modal_is_open: bool,
):
    current_device_list_children = Patch()
    if n_clicks_create_device and device_name and validate_ip_address(device_ip) and validate_port(device_port):
        device = models.DeviceCreate(ip=device_ip, port=device_port, name=device_name)
        db_device = device_cache.insert(device)

        if not db_device:
            return (
                current_device_list_children,
                modal_is_open,
                True,
            )

        current_device_list_children.append(render_device(db_device))

        return (
            current_device_list_children,
            not modal_is_open,
            False,
        )

    return (
        current_device_list_children,
        modal_is_open,
        True,
    )


@app.callback(
    Output(ids.DEVICE_LIST, "children", allow_duplicate=True),
    Input(ids.REFRESH, "n_clicks"),
    prevent_initial_call=True,
)
def refresh_device_list(_: int):
    return get_current_device_list()


@app.callback(
    Output(ids.DEVICE_LIST, "children", allow_duplicate=True),
    Input(ids.SCAN_DEVICES_BUTTON, "n_clicks"),
    State(ids.DEVICE_LIST, "children"),
    prevent_initial_call=True,
)
def scan_for_devices(_: int, current_children):
    dotenv.load_dotenv()

    network = os.getenv("NETWORK", "192.168.0.0/24")
    port = int(os.getenv("PORT", "8000"))
    print(f"Scanning network {network} on port {port}")
    logging.info("Scanning network %s on port %s", network, port)
    scan = networkscan.Networkscan(network)
    # This will cause problems if the scan takes longer than 30s"
    scan.run()

    device_list = current_children
    for host in scan.list_of_hosts_found:
        device = models.DeviceCreate(ip=host, port=port, name=host)

        if not api.validate_device_connection(device):
            continue

        db_device = device_cache.insert(device)
        device_list.append(render_device(db_device))

    return dbc.ListGroup(children=device_list, id=ids.DEVICE_LIST)
