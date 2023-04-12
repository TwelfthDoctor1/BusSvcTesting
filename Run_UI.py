import os
from dotenv import load_dotenv
from pathlib import Path
from UI.TransportUI import parse_to_ui

ENV_PATH = os.path.join(Path(__file__).resolve().parent, "RefKey.env")


# Load ENV
load_dotenv(dotenv_path=ENV_PATH)

# Get Values from ENV
API_KEY_LTA = os.getenv("API_KEY_LTA")
TIMING_URL = os.getenv("API_BUS_ARRIVAL_URL")
BUS_STOP_URL = os.getenv("API_BUS_STOP_URL")
ENV_LIST = [API_KEY_LTA, TIMING_URL, BUS_STOP_URL]

# Parse Data to UI
parse_to_ui(ENV_LIST)
