import logging
from typing import Union

import dash_bootstrap_components as dbc
from dash import dcc, html

from app import models
from app.components.alert import invalid_input_alert

logger = logging.getLogger("root")


def create_settings_modal(rts_id: int, device_id: int) -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Tracking Settings")),
                    dbc.ModalBody(
                        create_settings_form(rts_id=rts_id, device_id=device_id),
                        id={
                            "type": "settings-modal-body",
                            "rts_id": rts_id,
                            "device_id": device_id,
                        },
                    ),
                    dbc.ModalFooter(
                        children=html.Div(
                            [
                                dbc.Button(
                                    "Apply",
                                    id={
                                        "type": "apply-settings-modal",
                                        "rts_id": rts_id,
                                        "device_id": device_id,
                                    },
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Close",
                                    id={
                                        "type": "close-settings-modal",
                                        "rts_id": rts_id,
                                        "device_id": device_id,
                                    },
                                    className="ms-auto",
                                    n_clicks=0,
                                ),
                            ],
                            className="modal-footer-buttons",
                        ),
                    ),
                ],
                id={"type": "settings-modal", "rts_id": rts_id, "device_id": device_id},
                is_open=False,
            ),
        ]
    )


def create_settings_form(
    rts_id: int, device_id: int, tracking_settings: Union[None, models.TrackingSettings] = models.TrackingSettings()
) -> html.Div:
    if tracking_settings is None:
        tracking_settings = models.TrackingSettings()

    return html.Div(
        [
            invalid_input_alert(
                {
                    "type": "invalid-settings-input-alert",
                    "rts_id": rts_id,
                    "device_id": device_id,
                }
            ),
            dbc.Form(
                [
                    html.Div(
                        [
                            dbc.Label("Measurement Mode"),
                            dcc.Dropdown(
                                options=models.TrackingSettings().measurement_mode_options,
                                id={
                                    "type": "rts-measurement-mode",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.tmc_measurement_mode,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Inclination Mode"),
                            dcc.Dropdown(
                                options=models.TrackingSettings().inclination_mode_options,
                                id={
                                    "type": "rts-inclination-mode",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.tmc_inclination_mode,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("EDM Measurement Mode"),
                            dcc.Dropdown(
                                options=models.TrackingSettings().edm_measurement_mode_options,
                                id={
                                    "type": "rts-edm-mode",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.edm_measurement_mode,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Prism Type"),
                            dcc.Dropdown(
                                options=models.TrackingSettings().prism_type_options,
                                id={
                                    "type": "rts-prism-type",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.prism_type,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Fine Adjust Horizontal Search Range in rad"),
                            dbc.Input(
                                type="number",
                                id={
                                    "type": "rts-fine-adjust-horizontal-search-range",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.fine_adjust_horizontal_search_range,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Fine Adjust Vertical Search Range in rad"),
                            dbc.Input(
                                type="number",
                                id={
                                    "type": "rts-fine-adjust-vertical-search-range",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.fine_adjust_vertical_search_range,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Max Power Search Range in meters"),
                            dbc.Input(
                                type="number",
                                id={
                                    "type": "rts-power-search-range",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.power_search_max_range,
                                min=1,
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Power Search Enabled"),
                            dbc.Checkbox(
                                id={
                                    "type": "rts-power-search-enabled",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                                value=tracking_settings.power_search,
                            ),
                        ],
                        className="mb-3",
                    ),
                ],
            ),
        ]
    )
