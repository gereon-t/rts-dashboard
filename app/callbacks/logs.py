import logging

from dash import ALL, Input, Output, State, ctx

from app import api, app
from app.components import ids
from app.utils import DeviceNotFound, get_device_from_storage, logs_to_dropdown_options

logger = logging.getLogger("root")


@app.callback(
    Output(ids.LOG_MODAL, "is_open", allow_duplicate=True),
    Output(ids.LOG_DROPDOWN, "options", allow_duplicate=True),
    Output(ids.ACTIVE_DEVICE, "data", allow_duplicate=True),
    Output(ids.ACTIVE_RTS, "data", allow_duplicate=True),
    Input({"type": "rts-logs", "rts_id": ALL, "device_id": ALL}, "n_clicks"),
    Input(ids.CLOSE_LOG_MODAL_BUTTON, "n_clicks"),
    State(ids.LOG_MODAL, "is_open"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def toggle_modal(
    n_clicks: list[int],
    n_clicks_close: int,
    is_open: bool,
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the logs button of an RTS.

    It opens the logs modal and loads the current logs from the device.
    The current device is determined using the trigger context. The device id is
    stored in the active device store.

    Args:
        n_clicks (list): List of n_clicks for all logs buttons
        n_clicks_close (int): n_clicks for the close button
        is_open (bool): Current state of the modal
        device_storage (dict[str, dict]): Dictionary containing all devices

    Returns:
        tuple: Tuple containing the new state of the modal, the current logs and the
            active device id
    """
    if not any(n_clicks) and not (n_clicks_close > 0):
        modal_state = False
    else:
        modal_state = not is_open

    options: list[dict] = []
    button_id = ctx.triggered_id

    if not modal_state or button_id is None:
        return False, options, None, None

    device_id = button_id["device_id"]
    rts_id = button_id["rts_id"]

    try:
        device = get_device_from_storage(
            device_id=device_id, device_storage=device_storage
        )
    except DeviceNotFound:
        logger.error("Unable to get tracking settings")
        return modal_state, options, device_id, rts_id

    log_list = api.get_logs(device=device, rts_id=rts_id)
    options = logs_to_dropdown_options(log_list)

    return modal_state, options, device_id, rts_id


@app.callback(
    Output(ids.LOG_MODAL, "is_open", allow_duplicate=True),
    Output(ids.LOG_DOWNLOAD, "data"),
    Input(ids.DOWNLOAD_LOG, "n_clicks"),
    State(ids.LOG_MODAL, "is_open"),
    State(ids.LOG_DROPDOWN, "value"),
    State(ids.ACTIVE_DEVICE, "data"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def download_log(
    _: int,
    is_open: bool,
    log_id: int | None,
    device_id: int,
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the download button of the log
    modal.

    It downloads the log from the device and returns it as a download.

    Args:
        _: n_clicks of the download button
        is_open: Current state of the modal
        log_id: Id of the log to download
        device_id: Id of the device
        device_storage: Dictionary containing all devices

    Returns:
        tuple: Tuple containing the new state of the modal and the download data
    """
    if log_id is None:
        return is_open, None

    logger.info("Downloading log %i from device %i", log_id, device_id)

    try:
        device = get_device_from_storage(
            device_id=device_id, device_storage=device_storage
        )
    except DeviceNotFound:
        logger.error("Unable to get device %i", device_id)
        return is_open, None

    log_content = api.download_log(device=device, log_id=log_id)

    if log_content is None:
        logger.error("Failed to download log")
        return is_open, None

    return not is_open, dict(
        content=str(log_content, encoding="utf-8"), filename=f"log_{log_id}.txt"
    )


@app.callback(
    Output(ids.LOG_DROPDOWN, "options", allow_duplicate=True),
    Input(ids.DELETE_LOG, "n_clicks"),
    State(ids.LOG_DROPDOWN, "options"),
    State(ids.LOG_DROPDOWN, "value"),
    State(ids.ACTIVE_DEVICE, "data"),
    State(ids.ACTIVE_RTS, "data"),
    State(ids.DEVICE_STORAGE, "data"),
    prevent_initial_call=True,
)
def delete_log(
    n_clicks: int,
    options: list[dict],
    log_id: int | None,
    device_id: int,
    rts_id: int,
    device_storage: dict[str, dict],
):
    """
    This callback is triggered when the user clicks on the delete button of the log
    modal.

    It deletes the log from the device and updates the log dropdown.

    Args:
        n_clicks: n_clicks of the delete button
        options: Current options of the log dropdown
        log_id: Id of the log to delete
        device_id: Id of the device
        rts_id: Id of the RTS
        device_storage: Dictionary containing all devices

    Returns:
        dict: New options of the log dropdown
    """
    if log_id is None or not n_clicks:
        return options

    try:
        device = get_device_from_storage(
            device_id=device_id, device_storage=device_storage
        )
    except DeviceNotFound:
        logger.error("Unable to get device %i", device_id)
        return options

    response = api.delete_log(device=device, log_id=log_id)

    if not response:
        logger.error("Failed to delete log %i", log_id)
        return options

    logger.info("Deleted log %i from rts %i on device %i", log_id, rts_id, device_id)

    log_list = api.get_logs(device, rts_id)
    options = logs_to_dropdown_options(log_list)
    return options
