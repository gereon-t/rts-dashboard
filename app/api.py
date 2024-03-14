import logging
from typing import Optional, Union
import requests
from app import models

logger = logging.getLogger("root")


def request(
    device: models.DeviceCreate,
    method: str,
    path: str,
    json: Optional[dict] = None,
    timeout: float = 1.0,
) -> Union[requests.Response, None]:
    try:
        response = requests.request(
            method,
            f"http://{device.ip}:{device.port}{path}",
            json=json,
            timeout=timeout,
        )

        if response.status_code != 200:
            logger.error(response.text)
            return None

        return response
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        logger.error(
            "Failed to connect to device with ip: %s and port: %s",
            device.ip,
            device.port,
        )
        return None


def validate_device_connection(device: models.DeviceCreate) -> bool:
    response = request(device, "GET", "/", timeout=0.25)

    if response is None:
        return False

    response_json = response.json()
    if response_json is None or not isinstance(response_json, dict):
        return False

    return response_json.get("message", "") == "Server is running"


def add_rts(
    device: models.Device, rts: models.RTS_APICreate
) -> Union[models.RTS_API, None]:
    response = request(device, "POST", "/rts/", json=rts.model_dump())

    if response is None:
        logger.error("Failed to add rts %s", rts.name)
        return None

    logger.info("Added rts %s", rts.name)
    return models.RTS_API(**response.json())


def delete_rts(device: models.Device, rts_id: int) -> bool:
    response = request(device, "DELETE", f"/rts/{rts_id}")

    if response is None:
        return False

    logger.info("Deleted rts with id: %s", rts_id)
    return True


def delete_log(device: models.Device, log_id: int) -> bool:
    response = request(device, "DELETE", f"/logs/{log_id}")

    if response is None:
        return False

    logger.info("Deleted log with id: %s", log_id)
    return True


def get_rts(device: models.Device) -> list[models.RTS_API]:
    response = request(device, "GET", "/rts/")

    if response is None:
        return []

    return [models.RTS_API(**rts) for rts in response.json()]


def validate_rts_connection(device: models.Device, rts_id: int) -> bool:
    response = request(device, "GET", f"/rts/test/{rts_id}")

    if response is None:
        return False

    return True


def start_tracking(device: models.Device, rts_id: int) -> bool:
    response = request(device, "POST", f"/tracking/start/{rts_id}")

    if response is None:
        return False

    return True


def start_dummy_tracking(device: models.Device, rts_id: int) -> bool:
    response = request(device, "POST", f"/tracking/start/dummy/{rts_id}")

    if response is None:
        return False

    return True


def stop_tracking(device: models.Device, rts_id: int) -> bool:
    response = request(device, "POST", f"/tracking/stop/{rts_id}")

    if response is None:
        return False

    return True


def get_tracking_status(device: models.Device, rts_id: int) -> Union[dict, None]:
    response = request(device, "GET", f"/tracking/status/{rts_id}")

    if response is None:
        return None

    return response.json()


def get_connection_status(device: models.Device, rts_id: int) -> Union[dict, None]:
    response = request(device, "GET", f"/rts/status/{rts_id}")

    if response is None:
        return None

    return response.json()


def ping_rts(device: models.Device, rts_id: int) -> bool:
    response = request(device, "GET", f"/rts/ping/{rts_id}")

    if response is None:
        return False

    return True


def change_face(device: models.Device, rts_id: int) -> bool:
    response = request(device, "POST", f"/tracking/change_face/{rts_id}")

    if response is None:
        return False

    return True


def get_logs(device: models.Device, rts_id: int) -> list[models.Log]:
    response = request(device, "GET", f"/logs/rts/{rts_id}")

    if response is None:
        return []

    return [models.Log(**log) for log in response.json()]


def download_log(device: models.Device, log_id: int) -> Union[bytes, None]:
    response = request(device, "GET", f"/logs/download/{log_id}")

    if response is None:
        return None

    return response.content


def get_tracking_settings(device: models.Device, rts_id: int) -> Union[dict, None]:
    response = request(device, "GET", f"/tracking/settings/{rts_id}")

    if response is None:
        return None

    return response.json()


def update_tracking_settings(
    device: models.Device, rts_id: int, tracking_settings: models.TrackingSettings
) -> bool:
    response = request(
        device,
        "PUT",
        f"/tracking/settings/{rts_id}",
        json=tracking_settings.model_dump(),
    )

    if response is None:
        return False

    return True


def turn_to_target(
    device: models.Device, rts_id: int, target_position: models.Position
) -> bool:
    response = request(
        device,
        "PUT",
        f"/rts/turnto/{rts_id}",
        json=target_position.model_dump(),
    )

    if response is None:
        return False

    return True
