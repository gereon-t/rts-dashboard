import logging

import dash_bootstrap_components as dbc
from dash import dcc, html

from app import models
from app.components import ids

logger = logging.getLogger("root")


def rts_listgroup() -> list[html.Div]:
    return dbc.ListGroup(children=[], id=ids.RTS_LIST)


def render_rts(rts: models.RTS_API, device: models.Device) -> html.Div:
    return html.Div(
        className="list-item-container",
        children=[
            dcc.Store(
                data={"timestamp": 0, "pos_x": 0, "pos_y": 0, "pos_z": 0},
                id={
                    "type": "rts-position-storage",
                    "rts_id": rts.id,
                    "device_id": device.id,
                },
            ),
            html.Div(
                className="item-left-section",
                children=[
                    html.Img(
                        className="item-icon",
                        src="/assets/total-station.png",
                    ),
                    html.Div(
                        children=[
                            html.P(rts.name, className="item-name"),
                            html.P(f"Port: {rts.port}", className="item-detail"),
                            html.P(f"ID: {rts.id}", className="item-detail"),
                            html.P(f"Device: {device.name}", className="item-detail"),
                        ],
                        className="item-name-container",
                    ),
                ],
            ),
            html.Div(className="item-divider"),
            html.Div(
                className="item-middle-section",
                children=[
                    html.Div(
                        [
                            html.P(
                                "Serial Connection",
                                className="item-status-label",
                                id={
                                    "type": "rts-serial-status-label",
                                    "rts_id": rts.id,
                                    "device_id": device.id,
                                },
                            ),
                            html.Img(
                                className="item-status-icon",
                                src="/assets/status-unknown.svg",
                                id={
                                    "type": "rts-serial-status-icon",
                                    "rts_id": rts.id,
                                    "device_id": device.id,
                                },
                            ),
                        ],
                        className="item-status-row",
                    ),
                    html.Div(
                        [
                            html.P(
                                "Operation in Progress",
                                className="item-status-label",
                                id={
                                    "type": "rts-tracking-status-label",
                                    "rts_id": rts.id,
                                    "device_id": device.id,
                                },
                            ),
                            html.Img(
                                className="item-status-icon",
                                src="/assets/status-error.svg",
                                id={
                                    "type": "rts-tracking-status-icon",
                                    "rts_id": rts.id,
                                    "device_id": device.id,
                                },
                            ),
                            dcc.Interval(
                                id={
                                    "type": "rts-tracking-status-interval",
                                    "rts_id": rts.id,
                                    "device_id": device.id,
                                },
                                interval=1000,
                                n_intervals=0,
                            ),
                        ],
                        className="item-status-row",
                    ),
                ],
            ),
            html.Div(className="item-divider"),
            html.Div(
                className="item-right-section",
                children=[
                    html.Div(
                        children=[
                            html.P(
                                "Recorded Positions:", className="item-position-label"
                            ),
                            html.P(
                                0,
                                className="item-position-count",
                                id={
                                    "type": "rts-position-count",
                                    "rts_id": rts.id,
                                    "device_id": device.id,
                                },
                            ),
                        ],
                        className="item-position-row",
                    ),
                    html.Div(
                        children=[
                            html.P("Target Position:", className="item-position-label"),
                            html.P(
                                "0.00, 0.00, 0.00",
                                className="item-position-field",
                                id={
                                    "type": "rts-target-position",
                                    "rts_id": rts.id,
                                    "device_id": device.id,
                                },
                            ),
                        ],
                        className="item-position-row",
                    ),
                ],
            ),
            rts_actions(rts_id=rts.id, device_id=device.id),
        ],
        id={"type": "rts-item", "rts_id": rts.id, "device_id": device.id},
    )


def rts_actions(rts_id: int, device_id: int) -> html.Div:
    return html.Div(
        [
            dbc.ButtonGroup(
                [
                    dbc.Button(
                        "Logs",
                        id={
                            "type": "rts-logs",
                            "rts_id": rts_id,
                            "device_id": device_id,
                        },
                    ),
                    dbc.Button(
                        "Settings",
                        id={
                            "type": "rts-settings",
                            "rts_id": rts_id,
                            "device_id": device_id,
                        },
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem(
                                "Test Connection",
                                id={
                                    "type": "rts-test",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                            ),
                            dbc.DropdownMenuItem(
                                "Start Tracking",
                                id={
                                    "type": "rts-start",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                            ),
                            dbc.DropdownMenuItem(
                                "Stop Tracking",
                                id={
                                    "type": "rts-stop",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                            ),
                            dbc.DropdownMenuItem(
                                "Change Face",
                                id={
                                    "type": "rts-change-face",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                            ),
                            dbc.DropdownMenuItem(
                                "Remove",
                                id={
                                    "type": "rts-remove",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                            ),
                            dbc.DropdownMenuItem(
                                "Dummy Tracking",
                                id={
                                    "type": "rts-dummy",
                                    "rts_id": rts_id,
                                    "device_id": device_id,
                                },
                            ),
                        ],
                        label="Actions",
                        group=True,
                    ),
                ],
                vertical=True,
            ),
        ]
    )
