import dash_bootstrap_components as dbc
from dash import html

from app.components import ids
from app.components.device import create_device_list
from app.components.device_modal import device_form_modal
from app.components.rts import rts_listgroup
from app.components.rts_modal import rts_form_modal


def create_layout() -> html.Div:
    return html.Div(
        className="app-container",
        children=[
            create_header(),
            create_content(),
            create_footer(),
        ],
    )


def create_header() -> html.Header:
    return html.Header(
        className="header",
        children=[
            html.Div(
                className="left-section",
                children=[
                    html.A(
                        html.Div("RTS Dashboard", className="app-name"),
                        href="https://github.com/gereon-t/rts-dashboard",
                        style={"text-decoration": "none"},
                    ),
                ],
            ),
        ],
    )


def create_footer() -> html.Footer:
    return html.Footer(
        className="footer",
        children=[
            html.A(
                "gereon-t/rts-dashboard",
                href="https://github.com/gereon-t/rts-dashboard",
            ),
            html.Div(className="footer-divider"),
            html.A(
                "Device Icon by Hopstarter",
                href="https://www.flaticon.com/free-icons/raspberry-pi",
            ),
            html.Div(className="footer-divider"),
            html.A(
                "TS Icon by Freepik",
                href="https://www.flaticon.com/free-icons/topography",
            ),
        ],
    )


def create_content() -> html.Div:
    return html.Div(
        className="tab",
        children=[
            html.Div(
                className="tab-header-group",
                children=[
                    html.P("Logging Devices", className="section-header"),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Add Logging Device",
                                id=ids.OPEN_DEVICE_MODAL_BUTTON,
                                color="primary",
                                outline=True,
                            ),
                            dbc.Button(
                                "Scan for Devices",
                                id=ids.SCAN_DEVICES_BUTTON,
                                color="primary",
                                outline=True,
                            ),
                            dbc.Button(
                                "Refresh",
                                id=ids.REFRESH,
                                color="primary",
                                outline=True,
                            ),
                        ]
                    ),
                ],
            ),
            device_form_modal(),
            rts_form_modal(),
            create_device_list(),
            html.Div(className="tab-divider"),
            html.P("", id=ids.DUMMY_OUTPUT, style={"display": "none"}),
            html.Div(
                className="tab-header-group",
                children=[
                    html.P("Robotic Total Stations", className="section-header"),
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Add RTS",
                                id=ids.OPEN_RTS_MODAL_BUTTON,
                                color="primary",
                                outline=True,
                            ),
                            dbc.Button(
                                "Start All",
                                id=ids.START_ALL_BUTTON,
                                color="primary",
                                outline=True,
                            ),
                            dbc.Button(
                                "Stop All",
                                id=ids.STOP_ALL_BUTTON,
                                color="primary",
                                outline=True,
                            ),
                        ]
                    ),
                ],
            ),
            rts_listgroup(),
        ],
    )
