import datetime
import gzip
import json
import os
import urllib.request
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = os.path.join(Path(__file__).resolve().parent.parent, "RefKey.env")

# User Config
BUS_STOP = 77009

# Load ENV
load_dotenv(dotenv_path=ENV_PATH)

# Get Values from ENV
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_BUS_STOP_URL")

URL = f"{API_URL}"
headers = {
    "AccountKey": API_KEY,
    "accept": "application/json",
    "Content-Encoding": "gzip",
    "Transfer-Encoding": "chunked"
}

if __name__ == "__main__":
    REQUEST = urllib.request.Request(url=URL, headers=headers, method="GET")

    with urllib.request.urlopen(REQUEST) as response:
        json_dict = response.read().decode("utf-8")
        #post_json = json.dumps()

        dict_data = json.loads(json_dict)
        print(dict_data)

        for bus_stop_data in dict_data["value"]:
            #print(bus_stop_data)
            if bus_stop_data["BusStopCode"] == str(BUS_STOP):
                print(bus_stop_data["Description"])
                exit()
