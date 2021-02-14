from time import sleep, time
import requests
from requests import HTTPError

# Local Modules
import settings.dev as config
from sensors import dht_sensor
from relays import hvac
from services.oauth2.service import get_oauth2_token
from services.oauth_service import get_oauth_token
from services.utils import c_to_f

DHT22_1 = dht_sensor.DHT_SENSOR("DHT22", temp_format="C")
SYSTEM_STATE: str = config.SYSTEM_STATE
temp: float = config.temp
humidity: float = config.humidity
sensor_data: dict = config.sensor_data
TEMP_GOAL: str = config.TEMP_GOAL
HEAT_SETTING: int = config.HEAT_SETTING
COOL_SETTING: int = config.COOL_SETTING
ACTIVE_SLEEP_LIMIT: int = config.ACTIVE_SLEEP_LIMIT
ACTIVE_SLEEP_COUNTER: int = config.ACTIVE_SLEEP_COUNTER
CLIENT_ACCESS_KEY: str = config.CLIENT_ACCESS_KEY
CLIENT_SECRET_KEY: str = config.CLIENT_SECRET_KEY

OAUTH_DATA: dict = None


def set_oauth_data():
    global OAUTH_DATA
    now = time()
    oauth_resp = get_oauth_token(CLIENT_ACCESS_KEY, CLIENT_SECRET_KEY)
    OAUTH_DATA = {
        "access_token": oauth_resp["access_token"],
        "expiration": now + oauth_resp["expires_in"],
    }


def read_sensor(sensor: dht_sensor.DHT_SENSOR):
    result = sensor.read_sensor()
    # print(result)
    global sensor_data
    global temp
    global humidity
    try:
        temp = float(result[0])
        hum = float(result[1])
        sensor_data = {"temp": temp, "humidity": hum}
        try:
            global OAUTH_DATA
            print("Making requests to Artoo Hub")

            # if there is an access token and it is not expired, use it
            # else get a new token
            if OAUTH_DATA is None:
                set_oauth_data()
            elif OAUTH_DATA["expiration"] < now:
                set_oauth_data()

                # if OAUTH_DATA["expiration"] < now:
                # get new access_token

            HEADERS: dict = {
                "Authorization": f'Bearer {OAUTH_DATA["access_token"]}',
                "Content-Type": "application/json",
            }
            # This will eventually match to the main hub hostname
            # These requests need to match against the config for the particular hostname including the sensor_id, and types, along with auth code
            response = requests.post(
                "http://localhost:8000/api/sensors/data/",
                json={"name": "temperature", "values": temp, "sensor_id": 1},
                headers=HEADERS,
            )
            response2 = requests.post(
                "http://localhost:8000/api/sensors/data/",
                json={"name": "humidity", "values": hum, "sensor_id": 1},
                headers=HEADERS,
            )
        except HTTPError as error:
            print(error)
        finally:
            return sensor_data
    except:
        print("Error when reading sensor")
        sleep(2)
        read_sensor(sensor)

def temp_in_range(check_delay, active_delay):
    global SYSTEM_STATE
    global ACTIVE_SLEEP_LIMIT
    global ACTIVE_SLEEP_COUNTER

    print("Temperature is in range.")
    if SYSTEM_STATE == "ACTIVE":
        print("Turning off system")
        # turn system off since temp in range
        SYSTEM_STATE = "INACTIVE"
        # turn off appropriate relays
    else:
        SYSTEM_STATE = "INACTIVE"
    print("Delaying next check")
    # real delay will be ~ 2 minutes
    sleep(check_delay)


def temp_outof_range(check_delay, active_delay):
    global SYSTEM_STATE
    global ACTIVE_SLEEP_LIMIT
    global ACTIVE_SLEEP_COUNTER

    print("Temperature is out of range.")
    # keep track of 'ACTIVE' state
    print("Checking settings...")
    if SYSTEM_STATE == "ACTIVE":
        print("system already active")
        print("System waiting: {}s", format(active_delay))
        sleep(active_delay)
        ACTIVE_SLEEP_COUNTER += 1
        if ACTIVE_SLEEP_COUNTER > ACTIVE_SLEEP_LIMIT:
            print(
                "Limit of {} tries reached. System shutoff.", format(ACTIVE_SLEEP_LIMIT)
            )
            SYSTEM_STATE = "SHUTOFF"
    else:
        print("Verifying and activating system")
        SYSTEM_STATE = "ACTIVE"
        # activate relays
        hvac.test_relays()
        # real delay will be > 2 minutes
        sleep(check_delay)


def main():
    global SYSTEM_STATE
    global temp
    global humidity
    global sensor_data
    global TEMP_GOAL
    global HEAT_SETTING
    global COOL_SETTING
    check_delay = 300
    active_delay = 500
    global ACTIVE_SLEEP_LIMIT
    global ACTIVE_SLEEP_COUNTER

    while True:
        try:
            print("SYSTEM STATE: {}".format(SYSTEM_STATE))
            sensor_data = read_sensor(DHT22_1)
            if sensor_data is not None:
                temp = int(c_to_f(sensor_data["temp"]))
                humidity = int(sensor_data["humidity"])
            RANGE = range(COOL_SETTING, HEAT_SETTING)
            goal = RANGE[0]

            if TEMP_GOAL == "COOL":
                goal = RANGE[0]
                if temp <= goal:
                    temp_in_range(check_delay, active_delay)
                else:
                    temp_outof_range(check_delay, active_delay)
            else:
                goal = RANGE[-1]
                if temp <= goal:
                    temp_outof_range(check_delay, active_delay)
                else:
                    temp_in_range(check_delay, active_delay)

        except RuntimeError as error:
            print("Runtime error, program stopped")
            print(error.args[0])
        except:
            sleep(check_delay)


if __name__ == "__main__":
    main()