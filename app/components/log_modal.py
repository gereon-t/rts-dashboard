import logging

import dash_bootstrap_components as dbc
from dash import dcc, html

from app.components import ids

logger = logging.getLogger("root")


def create_log_modal() -> html.Div:
    return html.Div(
        [
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Log Download")),
                    dbc.ModalBody(dcc.Dropdown(id=ids.LOG_DROPDOWN, options=[])),
                    dbc.ModalFooter(
                        children=html.Div(
                            [
                                dbc.Button(
                                    "Download",
                                    id=ids.DOWNLOAD_LOG,
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Delete",
                                    id=ids.DELETE_LOG,
                                    className="ms-auto",
                                    n_clicks=0,
                                    style={"margin-right": "5px"},
                                ),
                                dbc.Button(
                                    "Close",
                                    id=ids.CLOSE_LOG_MODAL_BUTTON,
                                    className="ms-auto",
                                    n_clicks=0,
                                ),
                            ],
                            className="modal-footer-buttons",
                        ),
                    ),
                    dcc.Download(id=ids.LOG_DOWNLOAD),
                ],
                id=ids.LOG_MODAL,
                is_open=False,
            ),
        ]
    )
