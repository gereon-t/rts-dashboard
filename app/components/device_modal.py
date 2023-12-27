import logging

import dash_bootstrap_components as dbc
from dash import html

from app.components import ids
from app.components.alert import invalid_input_alert

logger = logging.getLogger("root")


def ip_address_input() -> html.Div:
    return dbc.Input(
        type="text", placeholder="Enter IP Address", id=ids.DEVICE_IP_INPUT
    )


def port_input() -> html.Div:
    return dbc.Input(
        type="number", placeholder="Enter Port", value=8000, id=ids.DEVICE_PORT_INPUT
    )


def create_device_form() -> html.Div:
    return html.Div(
        [
            invalid_input_alert(ids.INVALID_DEVICE_INPUT_ALERT),
            dbc.Form(
                [
                    html.Div(
                        [
                            dbc.Label("Name", width="auto"),
                            dbc.Input(
                                type="text",
                                placeholder="Enter Name",
                                id=ids.DEVICE_NAME_INPUT,
                            ),
                        ],
                        className="me-3",
                    ),
                    html.Div(
                        [dbc.Label("IP Address", width="auto"), ip_address_input()],
                        className="me-3",
                    ),
                    html.Div(
                        [
                            dbc.Label("Port", width="auto"),
                            port_input(),
                        ],
                        className="me-3",
                    ),
                ]
            ),
        ]
    )


def device_form_modal() -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Add Logging Device")),
                    dbc.ModalBody(create_device_form()),
                    dbc.ModalFooter(
                        children=html.Div(
                            [
                                dbc.Button(
                                    "Add",
                                    id=ids.CREATE_DEVICE_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Close",
                                    id=ids.CLOSE_DEVICE_MODAL_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                ),
                            ],
                            className="modal-footer-buttons",
                        ),
                    ),
                ],
                id=ids.DEVICE_MODAL,
                is_open=False,
            ),
        ]
    )
