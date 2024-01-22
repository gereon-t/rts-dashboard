import logging

import dash_bootstrap_components as dbc
from dash import html, dcc
from app.components import ids
from app import models

logger = logging.getLogger("root")


def create_device_list() -> dbc.ListGroup:
    return dbc.ListGroup(children=[], id=ids.DEVICE_LIST)


def render_device(device: models.Device) -> html.Div:
    device_item = html.Div(
        className="list-item-container",
        children=[
            dcc.Interval(
                id={
                    "type": "device-status-interval",
                    "device_id": device.id,
                },
                interval=1000,
                n_intervals=0,
            ),
            dcc.Store(id={"type": "device-status-changed", "device_id": device.id}),
            html.Div(
                className="item-left-section",
                children=[
                    html.Img(className="item-icon", src="/assets/cpu.png"),
                    html.Div(
                        children=[
                            html.P(
                                device.name,
                                className="item-name",
                            ),
                            html.P(
                                f"IP: {device.ip}:{device.port}",
                                className="item-detail",
                            ),
                        ],
                        className="item-name-container",
                        id={"type": "device-name", "device_id": device.id},
                    ),
                ],
            ),
            html.Div(
                className="item-middle-section",
                children=[
                    html.Div(
                        [
                            html.P(
                                "Connection Status",
                                className="item-status-label",
                                id={
                                    "type": "device-status-label",
                                    "device_id": device.id,
                                },
                            ),
                            html.Img(
                                className="item-status-icon",
                                src="/assets/status-unknown.svg",
                                id={
                                    "type": "device-status-icon",
                                    "device_id": device.id,
                                },
                            ),
                        ],
                        className="item-status-row",
                    )
                ],
            ),
            html.Div(
                className="item-right-section",
                children=[
                    device_action(device_id=device.id),
                ],
            ),
        ],
        id={"type": "device-item", "device_id": device.id},
    )
    return device_item


def device_action(device_id: int) -> html.Div:
    return dbc.Button(
        "Remove",
        color="danger",
        id={"type": "device-remove", "device_id": device_id},
    )
