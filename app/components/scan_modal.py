import logging

import dash_bootstrap_components as dbc
from dash import html, dcc

from app.components import ids
from app.components.alert import invalid_input_alert

logger = logging.getLogger("root")


def network_input() -> html.Div:
    return dbc.Input(
        type="text",
        placeholder="Enter Network",
        id=ids.NETWORK_INPUT,
        value="192.168.0.0/24",
    )


def port_input() -> html.Div:
    return dbc.Input(
        type="number", placeholder="Enter Port", value=8000, id=ids.NETWORK_PORT_INPUT
    )


def create_network_form() -> html.Div:
    return html.Div(
        [
            invalid_input_alert(ids.INVALID_SCAN_INPUT_ALERT),
            dbc.Form(
                [
                    html.Div(
                        [dbc.Label("Network", width="auto"), network_input()],
                        className="me-3",
                    ),
                    dcc.Loading(children=[], id=ids.SCAN_DEVICE_LOADING),
                    html.Div(
                        [dbc.Label("Port", width="auto"), port_input()],
                        className="me-3",
                    ),
                ]
            ),
        ]
    )


def network_form_modal() -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Scan for Devices")),
                    dbc.ModalBody(create_network_form()),
                    dbc.ModalFooter(
                        children=html.Div(
                            [
                                dbc.Button(
                                    "Scan",
                                    id=ids.SCAN_DEVICE_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Close",
                                    id=ids.CLOSE_SCAN_MODAL_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                ),
                            ],
                            className="modal-footer-buttons",
                        ),
                    ),
                ],
                id=ids.SCAN_MODAL,
                is_open=False,
            ),
        ]
    )
