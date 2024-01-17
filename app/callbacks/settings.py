import logging

from dash import ALL, Input, Output, State, ctx

from app import api, app, models
from app.components import ids
from app.utils import DeviceNotFound, get_device_from_storage

logger = logging.getLogger("root")


@app.callback(
    Output(ids.SETTINGS_MODAL, "is_open", allow_duplicate=True),
    Output(ids.RTS_MEASUREMENT_MODE, "value"),
    Output(ids.RTS_INCLINATION_MODE, "value"),
    Output(ids.RTS_EDM_MODE, "value"),
    Output(ids.RTS_PRISM_TYPE, "value"),
    Output(ids.RTS_FINE_ADJUST_HORIZONTAL_SEARCH_RANGE, "value"),
    Output(ids.RTS_FINE_ADJUST_VERTICAL_SEARCH_RANGE, "value"),
    Output(ids.RTS_POWER_SEARCH_RANGE, "value"),
    Output(ids.RTS_POWER_SEARCH_ENABLED, "value"),
    Output(ids.ACTIVE_RTS, "data", allow_duplicate=True),
    Output(ids.ACTIVE_DEVICE, "data", allow_duplicate=True),
    Input({"type": "rts-settings", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    Input(ids.CLOSE_SETTINGS_MODAL_BUTTON, "n_clicks"),
    State(ids.SETTINGS_MODAL, "is_open"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def toggle_modal(
    n_clicks_settings: list,
    n_clicks_close: int,
    is_open: bool,
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the settings button of an RTS.

    It opens the settings modal and loads the current settings from the device.
    The current device is determined using the trigger context. For further logic
    regarding the settings modal, the device and RTS id are stored in the active
    device and active RTS store.

    Args:
        n_clicks_settings (list): List of n_clicks for all settings buttons
        n_clicks_close (int): n_clicks for the close button
        is_open (bool): Current state of the modal
        device_storage (dict[str, dict]): Dictionary containing all devices

    Returns:
        tuple: Tuple containing the new state of the modal, the current settings
            and the active RTS and device id
    """
    if not any(n_clicks_settings) and not (n_clicks_close > 0):
        modal_state = False
    else:
        modal_state = not is_open

    tracking_settings = models.TrackingSettings()

    if not modal_state:
        return modal_state, *tracking_settings.modal_tuple, None, None

    button_id = ctx.triggered_id
    device_id = button_id["device_id"]
    rts_id = button_id["rts_id"]

    try:
        device = get_device_from_storage(
            device_id=device_id, device_storage=device_storage
        )
        rts_api_settings = api.get_tracking_settings(device=device, rts_id=rts_id)
    except DeviceNotFound:
        logger.error("Unable to get tracking settings")
        rts_api_settings = None

    if rts_api_settings is not None:
        tracking_settings = models.TrackingSettings(**rts_api_settings)

    return modal_state, *tracking_settings.modal_tuple, rts_id, device_id


@app.callback(
    Output(ids.SETTINGS_MODAL, "is_open", allow_duplicate=True),
    Output(ids.INVALID_SETTINGS_INPUT_ALERT, "is_open"),
    Output(ids.INVALID_SETTINGS_INPUT_ALERT, "children"),
    Input(ids.APPLY_SETTINGS_MODAL_BUTTON, "n_clicks"),
    State(ids.RTS_MEASUREMENT_MODE, "value"),
    State(ids.RTS_INCLINATION_MODE, "value"),
    State(ids.RTS_EDM_MODE, "value"),
    State(ids.RTS_PRISM_TYPE, "value"),
    State(ids.RTS_FINE_ADJUST_HORIZONTAL_SEARCH_RANGE, "value"),
    State(ids.RTS_FINE_ADJUST_VERTICAL_SEARCH_RANGE, "value"),
    State(ids.RTS_POWER_SEARCH_RANGE, "value"),
    State(ids.RTS_POWER_SEARCH_ENABLED, "value"),
    State(ids.SETTINGS_MODAL, "is_open"),
    State(ids.DEVICE_STORAGE, "data"),
    State(ids.ACTIVE_RTS, "data"),
    State(ids.ACTIVE_DEVICE, "data"),
    prevent_initial_call=True,
)
def update_tracking_settings(
    n_clicks: int,
    measurement_mode: int,
    inclination_mode: int,
    edm_mode: int,
    prism_type: int,
    fine_adjust_horizontal_search_range: float,
    fine_adjust_vertical_search_range: float,
    power_search_range: int,
    power_search_enabled: bool,
    is_open: bool,
    device_storage: dict[str, dict],
    active_rts: int,
    active_device: int,
):
    """
    This callback is triggered when the user clicks on the apply button in the
    settings modal.

    Since there is only one apply button for all settings modals, the active RTS
    and device are determined using the active RTS and device store. Those stores
    are updated in the toggle_modal callback. Whenever the modal is opened, the
    active RTS and device are updated, ensuring that the correct settings are
    updated.

    Args:
        n_clicks (int): Number of clicks on the apply button
        measurement_mode (int): Measurement mode
        inclination_mode (int): Inclination mode
        edm_mode (int): EDM mode
        prism_type (int): Prism type
        fine_adjust_horizontal_search_range (float): Horizontal search range
        fine_adjust_vertical_search_range (float): Vertical search range
        power_search_range (int): Power search range
        power_search_enabled (bool): Power search enabled
        is_open (bool): Current state of the modal
        device_storage (dict[str, dict]): Dictionary containing all devices
        active_rts (int): Active RTS
        active_device (int): Active device

    Returns:
        tuple: Tuple containing the new state of the modal, the state of the alert
            and the alert message
    """
    if None in (active_rts, active_device):
        return is_open, True, "No active device or RTS"

    if not n_clicks:
        return is_open, False, None

    tracking_settings = models.TrackingSettings(
        tmc_measurement_mode=measurement_mode,
        tmc_inclination_mode=inclination_mode,
        edm_measurement_mode=edm_mode,
        prism_type=prism_type,
        fine_adjust_horizontal_search_range=fine_adjust_horizontal_search_range,
        fine_adjust_vertical_search_range=fine_adjust_vertical_search_range,
        power_search_max_range=power_search_range,
        power_search=power_search_enabled,
    )

    try:
        device = get_device_from_storage(
            device_id=active_device, device_storage=device_storage
        )
    except DeviceNotFound:
        return is_open, True, "Could not find device"

    response = api.update_tracking_settings(
        device=device,
        rts_id=active_rts,
        tracking_settings=tracking_settings,
    )

    if not response:
        return True, True, "Could not update tracking settings"

    return not is_open, False, None
