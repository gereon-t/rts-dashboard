import logging

import dash_bootstrap_components as dbc
from dash import dcc, html

logger = logging.getLogger("root")


def create_log_modal(rts_id: int, device_id: int) -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Log Download")),
                    dbc.ModalBody(
                        dcc.Dropdown(
                            id={
                                "type": "log-dropdown",
                                "rts_id": rts_id,
                                "device_id": device_id,
                            },
                            options=[],
                        )
                    ),
                    dbc.ModalFooter(
                        children=html.Div(
                            [
                                dbc.Button(
                                    "Download",
                                    id={
                                        "type": "download-log",
                                        "rts_id": rts_id,
                                        "device_id": device_id,
                                    },
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Delete",
                                    id={
                                        "type": "delete-log",
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
                                        "type": "close-log-modal",
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
                    dcc.Download(
                        id={
                            "type": "log-download",
                            "device_id": device_id,
                            "rts_id": rts_id,
                        }
                    ),
                ],
                id={"type": "log-modal", "rts_id": rts_id, "device_id": device_id},
                is_open=False,
            ),
        ]
    )
