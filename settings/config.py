SYSTEM_STATE = 'INITIAL'
TEMP_GOAL: str = 'HEAT'
HEAT_SETTING: int = 74
COOL_SETTING: int = 69
ACTIVE_SLEEP_LIMIT: int = 10
ACTIVE_SLEEP_COUNTER: int = 500

temp: float = None
humidity: float = None
sensor_data: dict = {}