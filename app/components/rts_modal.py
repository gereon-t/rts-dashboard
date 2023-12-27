import logging

import dash_bootstrap_components as dbc
from dash import dcc, html

from app.components import ids
from app.components.alert import invalid_input_alert

logger = logging.getLogger("root")


def create_rts_form() -> html.Div:
    return html.Div(
        [
            invalid_input_alert(ids.INVALID_RTS_INPUT_ALERT),
            dbc.Form(
                [
                    html.Div(
                        [
                            dbc.Label("Logging Device"),
                            dcc.Dropdown(id=ids.DEVICE_DROPDOWN),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Name"),
                            dbc.Input(
                                type="text",
                                id=ids.RTS_NAME_INPUT,
                                placeholder="Enter name",
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Port"),
                            dbc.Input(
                                type="text",
                                id=ids.RTS_PORT_INPUT,
                                value="/dev/ttyUSB0",
                                placeholder="Enter port",
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Baudrate"),
                            dbc.Input(
                                type="number",
                                id=ids.RTS_BAUDRATE_INPUT,
                                value="115200",
                                placeholder="Enter baudrate",
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Parity"),
                            dbc.Select(
                                id=ids.RTS_PARITY_INPUT,
                                options=[
                                    {"label": "None", "value": "N"},
                                    {"label": "Even", "value": "E"},
                                    {"label": "Odd", "value": "O"},
                                ],
                                value="N",
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Stopbits"),
                            dbc.Input(
                                type="number",
                                id=ids.RTS_STOPBITS_INPUT,
                                value="1",
                                min=0,
                                placeholder="Enter stopbits",
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Bytesize"),
                            dbc.Input(
                                type="number",
                                id=ids.RTS_BYTESIZE_INPUT,
                                value="8",
                                min=0,
                                placeholder="Enter bytesize",
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Timeout"),
                            dbc.Input(
                                type="number",
                                id=ids.RTS_TIMEOUT_INPUT,
                                value="30",
                                min=0,
                                placeholder="Enter timeout",
                            ),
                        ],
                        className="mb-3",
                    ),
                ],
            ),
        ]
    )


def rts_form_modal() -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Add RTS")),
                    dbc.ModalBody(create_rts_form()),
                    dbc.ModalFooter(
                        children=html.Div(
                            [
                                dbc.Button(
                                    "Add",
                                    id=ids.CREATE_RTS_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Close",
                                    id=ids.CLOSE_RTS_MODAL_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                ),
                            ],
                            className="modal-footer-buttons",
                        )
                    ),
                ],
                id=ids.RTS_MODAL,
                is_open=False,
            ),
        ]
    )
