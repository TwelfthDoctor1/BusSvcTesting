import os
from dotenv import load_dotenv
from pathlib import Path
from UI.TransportUI import parse_to_ui

ENV_PATH = os.path.join(Path(__file__).resolve().parent, "RefKey.env")


# Load ENV
load_dotenv(dotenv_path=ENV_PATH)

# Get Values from ENV
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_BUS_TIMING_URL")
ENV_LIST = [API_KEY, API_URL]

# Parse Data to UI
parse_to_ui(ENV_LIST)
