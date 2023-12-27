import logging

from app import device_cache, models

logger = logging.getLogger("root")


def to_dropdown_options(devices: list[models.Device]) -> list[dict]:
    return [{"label": device.name, "value": device.id} for device in devices]


def get_current_dropdown_options():
    devices = device_cache.get_all()
    return [{"label": device.name, "value": device.id} for device in devices]
