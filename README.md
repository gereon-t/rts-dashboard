<div align="center">
    <h1>Robotic Total Station Dashboard</h1>
    <a href="https://github.com/gereon-t/rts-dashboard/releases"><img src="https://img.shields.io/github/v/release/gereon-t/rts-dashboard?label=version" /></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" /></a>
    <a href="https://github.com/gereon-t/rts-dashboard/blob/main/LICENSE"><img src="https://img.shields.io/github/license/gereon-t/rts-dashboard" /></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

#### With RTS Dashboard you can easily control multiple RTS connected to logging devices within the same network.

<p align="center">
  <img style="border-radius: 10px;" src=.images/dashboard.png>
</p>

</div>

Device icon from [Hopstarter](https://www.flaticon.com/free-icons/raspberry-pi). RTS icon from [Freepik](https://www.flaticon.com/free-icons/topography).

# Installation

```bash
docker run -p 8050:8050 gtombrink/rts-dashboard
```

or using the docker-compose file:

```yaml
version: "3.8"
services:
  rts-dashboard:
    image: gtombrink/rts-dashboard
    ports:
      - 8050:8050
    restart: unless-stopped
```

```bash
docker-compose up -d
```

You can now access the dashboard at http://localhost:8050.

# Architecture

<img src=".images/structure.png" width=400/>

A single instance of the RTS Dashboard has the capability to oversee and manage multiple logging devices running the RTS Server, which will soon be available at https://github.com/gereon-t/rts-server. The RTS Server functions as an intermediary, receiving requests through a REST API and forwarding them to the associated RTS instances using serial communication. Additionally, the RTS Server collects data from the connected RTS devices and sends it to the RTS Dashboard if requested. The tasks of each connected RTS are managed by separate rq workers that read jobs from a Redis queue.
