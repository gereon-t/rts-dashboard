import logging

from dash import MATCH, Input, Output, State

from app import api, app, device_cache

logger = logging.getLogger("root")


@app.callback(
    Output(
        {"type": "log-modal", "rts_id": MATCH, "device_id": MATCH},
        "is_open",
        allow_duplicate=True,
    ),
    Output(
        {"type": "log-dropdown", "rts_id": MATCH, "device_id": MATCH},
        "options",
        allow_duplicate=True,
    ),
    Input({"type": "rts-logs", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "close-log-modal", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "rts-logs", "rts_id": MATCH, "device_id": MATCH}, "id"),
    State({"type": "log-modal", "rts_id": MATCH, "device_id": MATCH}, "is_open"),
    State({"type": "log-dropdown", "rts_id": MATCH, "device_id": MATCH}, "options"),
    prevent_initial_call=True,
)
def toggle_modal(n1, n2, trigger_info, is_open, options):
    if n1 or n2:
        return_state = not is_open
    else:
        return_state = is_open

    if return_state:
        device_id = trigger_info["device_id"]
        rts_id = trigger_info["rts_id"]
        log_list = api.get_logs(device_cache.get(device_id), rts_id)
        options = [
            {"label": f"{log.name}: {log.path}", "value": log.id} for log in log_list
        ]
        return return_state, options

    return return_state, options


@app.callback(
    Output(
        {"type": "log-modal", "rts_id": MATCH, "device_id": MATCH},
        "is_open",
        allow_duplicate=True,
    ),
    Output({"type": "log-download", "device_id": MATCH, "rts_id": MATCH}, "data"),
    Input({"type": "download-log", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "download-log", "rts_id": MATCH, "device_id": MATCH}, "id"),
    State({"type": "log-modal", "rts_id": MATCH, "device_id": MATCH}, "is_open"),
    State({"type": "log-dropdown", "rts_id": MATCH, "device_id": MATCH}, "value"),
    prevent_initial_call=True,
)
def download_log(n_clicks, trigger_info, is_open, log_id):
    if n_clicks and log_id:
        rts_id = trigger_info["rts_id"]
        device_id = trigger_info["device_id"]
        logger.info(
            "Downloading log %i from rts %i on device %i", log_id, rts_id, device_id
        )
        log_content = api.download_log(
            device=device_cache.get(device_id), log_id=log_id
        )
        return not is_open, dict(
            content=str(log_content, encoding="utf-8"),
            filename=f"rts_{rts_id}_log_{log_id}.txt",
        )

    return False, dict(content="", filename="")


@app.callback(
    Output(
        {"type": "log-dropdown", "rts_id": MATCH, "device_id": MATCH},
        "options",
        allow_duplicate=True,
    ),
    Input({"type": "delete-log", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input({"type": "delete-log", "rts_id": MATCH, "device_id": MATCH}, "id"),
    State({"type": "log-dropdown", "rts_id": MATCH, "device_id": MATCH}, "options"),
    State({"type": "log-dropdown", "rts_id": MATCH, "device_id": MATCH}, "value"),
    prevent_initial_call=True,
)
def delete_log(n_clicks, trigger_info, options, log_id):
    if n_clicks and log_id:
        rts_id = trigger_info["rts_id"]
        device_id = trigger_info["device_id"]

        response = api.delete_log(device=device_cache.get(device_id), log_id=log_id)

        if not response:
            logger.error("Failed to delete log %i", log_id)
            return options

        logger.info(
            "Deleted log %i from rts %i on device %i", log_id, rts_id, device_id
        )

        log_list = api.get_logs(device_cache.get(device_id), rts_id)
        options = [
            {"label": f"{log.name}: {log.path}", "value": log.id} for log in log_list
        ]
        return options

    return options
