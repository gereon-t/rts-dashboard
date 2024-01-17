import logging

import dash_bootstrap_components as dbc
from dash import dcc, html

from app import models
from app.components import ids
from app.components.alert import invalid_input_alert

logger = logging.getLogger("root")


def create_settings_modal() -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Tracking Settings")),
                    dbc.ModalBody(create_settings_form(), id=ids.SETTINGS_MODAL_BODY),
                    dbc.ModalFooter(
                        children=html.Div(
                            [
                                dbc.Button(
                                    "Apply",
                                    id=ids.APPLY_SETTINGS_MODAL_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Close",
                                    id=ids.CLOSE_SETTINGS_MODAL_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                ),
                            ],
                            className="modal-footer-buttons",
                        ),
                    ),
                ],
                id=ids.SETTINGS_MODAL,
                is_open=False,
            ),
        ]
    )


def create_settings_form() -> html.Div:
    tracking_settings = models.TrackingSettings()
    return html.Div(
        [
            invalid_input_alert(ids.INVALID_SETTINGS_INPUT_ALERT),
            dbc.Form(
                [
                    html.Div(
                        [
                            dbc.Label("Measurement Mode"),
                            dcc.Dropdown(
                                options=models.TrackingSettings().measurement_mode_options,
                                id=ids.RTS_MEASUREMENT_MODE,
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
                                id=ids.RTS_INCLINATION_MODE,
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
                                id=ids.RTS_EDM_MODE,
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
                                id=ids.RTS_PRISM_TYPE,
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
                                id=ids.RTS_FINE_ADJUST_HORIZONTAL_SEARCH_RANGE,
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
                                id=ids.RTS_FINE_ADJUST_VERTICAL_SEARCH_RANGE,
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
                                id=ids.RTS_POWER_SEARCH_RANGE,
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
                                id=ids.RTS_POWER_SEARCH_ENABLED,
                                value=tracking_settings.power_search,
                            ),
                        ],
                        className="mb-3",
                    ),
                ],
            ),
        ]
    )
