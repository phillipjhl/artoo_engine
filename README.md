# ARTOO Engine

The core engine for running ARTOO main hub program for home automation.

This project also has libraries and APIs to integrate with a running webserver to send data recording from sensors for DB persistent storage and other integrations.

The artoo_engine program is optimized for running on Rasberry Pi boards so it can interop with local system modules that read sensor data including buses and GPIO pins.

Running the artoo_engine program via a `systemctl` boot process.

## Starting

Install all requirements.
`$ pipenv install`

Start shell within virtual environment.
`$ pipenv shell`

Start artoo engine.
`(artoo_engine) $ python artoo_engine/main.py`

### To Do

- [ ] Python code for sensor reading and PUB/SUB to ARTOO
    - [X] DHT11/22 sensor reading
    - [X] Relay activation
    - [ ] CO sensor reading
- [ ] HVAC scheduling
- [ ] IR motion sensors for lights and occupancy readings
- [ ] Temperature readings across the house to gauge appropriate air flow. Corresponding microcontrollers using stepper motors could be attached to air vents to then manage air flow based off of temp. readings