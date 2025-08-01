import os
from dotenv import load_dotenv
from pathlib import Path
from TransportAPI.BusStopInfo import store_bus_stop_data
from TransportAPI.BusService import store_bus_svc_data
from UI.TransportUI import parse_to_ui
from UtilLib.JSONHandler import setDebugState_JSONLib

ENV_PATH = os.path.join(Path(os.path.expanduser("~")).resolve(), "RefKey.env")


# Load ENV
load_dotenv(dotenv_path=ENV_PATH)

setDebugState_JSONLib(False, os.path.join(Path(os.path.expanduser("~")).resolve(), "JSONLib"))

# Get Values from ENV
API_KEY_LTA = os.getenv("API_KEY_LTA")
ENV_LIST = [API_KEY_LTA]

# Data Caching
store_bus_stop_data(API_KEY_LTA)
store_bus_svc_data(API_KEY_LTA)

# Parse Data to UI
parse_to_ui(ENV_LIST)
