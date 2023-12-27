from dash import MATCH, Input, Output, State

from app import api, app, device_cache, models
from app.components.settings_modal import create_settings_form


@app.callback(
    Output(
        {"type": "settings-modal", "rts_id": MATCH, "device_id": MATCH},
        "is_open",
        allow_duplicate=True,
    ),
    Output(
        {"type": "settings-modal-body", "rts_id": MATCH, "device_id": MATCH}, "children"
    ),
    Input({"type": "rts-settings", "rts_id": MATCH, "device_id": MATCH}, "n_clicks"),
    Input(
        {"type": "close-settings-modal", "rts_id": MATCH, "device_id": MATCH},
        "n_clicks",
    ),
    Input({"type": "rts-settings", "rts_id": MATCH, "device_id": MATCH}, "id"),
    State({"type": "settings-modal", "rts_id": MATCH, "device_id": MATCH}, "is_open"),
    prevent_initial_call=True,
)
def toggle_modal(n1, n2, trigger_info, is_open):
    if n1 or n2:
        return_value = not is_open
    else:
        return_value = is_open

    if return_value:
        rts_id = trigger_info["rts_id"]
        device_id = trigger_info["device_id"]
        rts_api_settings = api.get_tracking_settings(
            device=device_cache.get(device_id), rts_id=rts_id
        )

        if rts_api_settings is None:
            tracking_settings = models.TrackingSettings()
        else:
            tracking_settings = models.TrackingSettings(**rts_api_settings)
            
        return return_value, create_settings_form(
            rts_id=rts_id, device_id=device_id, tracking_settings=tracking_settings
        )

    return return_value, None


@app.callback(
    Output(
        {"type": "settings-modal", "rts_id": MATCH, "device_id": MATCH},
        "is_open",
        allow_duplicate=True,
    ),
    Output(
        {"type": "invalid-settings-input-alert", "rts_id": MATCH, "device_id": MATCH},
        "is_open",
    ),
    Output(
        {"type": "invalid-settings-input-alert", "rts_id": MATCH, "device_id": MATCH},
        "children",
    ),
    Input(
        {"type": "apply-settings-modal", "rts_id": MATCH, "device_id": MATCH},
        "n_clicks",
    ),
    Input({"type": "apply-settings-modal", "rts_id": MATCH, "device_id": MATCH}, "id"),
    State(
        {"type": "rts-measurement-mode", "rts_id": MATCH, "device_id": MATCH}, "value"
    ),
    State(
        {"type": "rts-inclination-mode", "rts_id": MATCH, "device_id": MATCH}, "value"
    ),
    State({"type": "rts-edm-mode", "rts_id": MATCH, "device_id": MATCH}, "value"),
    State({"type": "rts-prism-type", "rts_id": MATCH, "device_id": MATCH}, "value"),
    State(
        {
            "type": "rts-fine-adjust-horizontal-search-range",
            "rts_id": MATCH,
            "device_id": MATCH,
        },
        "value",
    ),
    State(
        {
            "type": "rts-fine-adjust-vertical-search-range",
            "rts_id": MATCH,
            "device_id": MATCH,
        },
        "value",
    ),
    State(
        {"type": "rts-power-search-range", "rts_id": MATCH, "device_id": MATCH}, "value"
    ),
    State(
        {"type": "rts-power-search-enabled", "rts_id": MATCH, "device_id": MATCH},
        "value",
    ),
    State({"type": "settings-modal", "rts_id": MATCH, "device_id": MATCH}, "is_open"),
    prevent_initial_call=True,
)
def update_tracking_settings(
    n_clicks: int,
    trigger_info: dict,
    measurement_mode: int,
    inclination_mode: int,
    edm_mode: int,
    prism_type: int,
    fine_adjust_horizontal_search_range: float,
    fine_adjust_vertical_search_range: float,
    power_search_range: int,
    power_search_enabled: bool,
    is_open: bool,
):
    if n_clicks:
        rts_id = trigger_info["rts_id"]
        device_id = trigger_info["device_id"]

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
        response = api.update_tracking_settings(
            device=device_cache.get(device_id),
            rts_id=rts_id,
            tracking_settings=tracking_settings,
        )

        if not response:
            return True, True, "Could not update tracking settings"

        return False, False, None

    return is_open, False, None
