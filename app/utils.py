import logging

from app import models

logger = logging.getLogger("root")


def to_dropdown_options(device_storage: dict[str, dict]) -> list[dict]:
    devices = [models.Device(**device) for device in device_storage.values()]
    return [{"label": device.name, "value": device.id} for device in devices]


def get_current_dropdown_options(device_storage: dict[str, dict]) -> list[dict]:
    return [
        {"label": device["name"], "value": device["id"]}
        for device in device_storage.values()
    ]


class DeviceNotFound(Exception):
    """Exception raised when a device is not found in the device storage."""


def get_device_from_storage(
    device_id: int, device_storage: dict[str, dict]
) -> models.Device:
    """
    This function returns the device with the given ID from the device storage.

    Args:
        device_id (int): The ID of the device
        device_storage (dict[str, dict]): The current device storage

    Returns:
        models.Device: The device with the given ID
    """
    if str(device_id) not in device_storage:
        raise DeviceNotFound(f"Device with ID {device_id} not found")

    return models.Device(**device_storage[str(device_id)])


def get_button_index(n_clicks: list[None | int]) -> int:
    """
    This function returns the index of the button that was clicked.

    Args:
        n_clicks (list): The number of times each button was clicked

    Returns:
        int: The index of the button that was clicked
    """
    return next(i for i, value in enumerate(n_clicks) if value is not None)
