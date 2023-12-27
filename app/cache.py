import logging

from app import models

logger = logging.getLogger("root")


class DeviceCache:
    device_count = 0

    def __init__(self):
        self.cache = {}

    def get(self, device_id: int) -> models.Device:
        return self.cache.get(device_id)

    def update(self, device: models.Device):
        if device.id not in self.cache:
            logger.info("Device %i not found in cache. No update performed.", device.id)
            return

        logger.info("Updating device %i", device.id)
        self.cache[device.id] = device

    def insert(self, device: models.DeviceCreate) -> models.Device:
        device = models.Device(id=DeviceCache.device_count, **device.model_dump())
        self.cache[device.id] = device
        DeviceCache.device_count += 1
        logger.info("Inserted device %i", device.id)
        return device

    def delete(self, device_id: int):
        logger.info("Deleting device %i", device_id)
        del self.cache[device_id]

    def get_all(self) -> list[models.Device]:
        return list(self.cache.values())

    def clear(self):
        logger.info("Clearing cache")
        self.cache.clear()
