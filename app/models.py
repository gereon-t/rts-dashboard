from pydantic import BaseModel


class RTS_APICreate(BaseModel):
    name: str
    baudrate: int
    port: str
    timeout: int
    parity: str
    stopbits: int
    bytesize: int


class RTS_API(RTS_APICreate):
    id: int


class RTS(BaseModel):
    id: int
    device_id: int
    name: str


class DeviceCreate(BaseModel):
    ip: str
    port: int
    name: str


class Device(DeviceCreate):
    id: int


class Log(BaseModel):
    id: int
    rts_id: int
    path: str
    active: bool
    name: str


class TrackingSettings(BaseModel):
    tmc_measurement_mode: int = 1
    tmc_inclination_mode: int = 1
    edm_measurement_mode: int = 9
    prism_type: int = 3
    fine_adjust_position_mode: int = 1
    fine_adjust_horizontal_search_range: float = 0.0872
    fine_adjust_vertical_search_range: float = 0.0872
    power_search_area_dcenterhz: float = 0.0
    power_search_area_dcenterv: float = 1.5708
    power_search_area_drangehz: float = 6.283
    power_search_area_drangev: float = 0.6
    power_search_area_enabled: int = 1
    power_search_min_range: int = 1
    power_search_max_range: int = 50
    power_search: bool = True

    @property
    def measurement_mode_options(self) -> list[dict]:
        return [
            {"label": "Default Distance", "value": 1},
            {"label": "Distance Tracking", "value": 2},
        ]

    @property
    def inclination_mode_options(self) -> list[dict]:
        return [
            {"label": "Use Sensor", "value": 0},
            {"label": "Automatic", "value": 1},
            {"label": "Use Plane", "value": 2},
        ]

    @property
    def edm_measurement_mode_options(self) -> list[dict]:
        return [
            {"label": "Continuous Standard", "value": 6},
            {"label": "Continuous Dynamic", "value": 7},
            {"label": "Continuous Reflectorless", "value": 8},
            {"label": "Continuous Fast", "value": 9},
        ]

    @property
    def prism_type_options(self) -> list[dict]:
        return [
            {"label": "Leica Round", "value": 0},
            {"label": "Leica Mini", "value": 1},
            {"label": "Leica Tape", "value": 2},
            {"label": "Leica 360", "value": 3},
            {"label": "Leica 360 Mini", "value": 7},
            {"label": "Leica Mini Zero", "value": 8},
            {"label": "Leica NDS Tape", "value": 10},
            {"label": "Leica GRZ121 Round", "value": 11},
            {"label": "Leica MPR122", "value": 12},
            {"label": "User Defined 1", "value": 4},
            {"label": "User Defined 2", "value": 5},
            {"label": "User Defined 3", "value": 6},
            {"label": "User Defined", "value": 9},
        ]

    @property
    def fine_adjust_position_mode_options(self) -> list[dict]:
        return [
            {"label": "Norm", "value": 0},
            {"label": "Point", "value": 1},
        ]
