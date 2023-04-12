import os
from dotenv import load_dotenv
from pathlib import Path
from TransportAPI.BusArrival import request_bus_stop_timing
from TransportAPI.BusStopInfo import request_bus_stop_name_lta

KEY_BUS_STOPS = ["77009", "77011", "77191", "65191", "65199"]

ENV_PATH = os.path.join(Path(__file__).resolve().parent, "RefKey.env")

# Load ENV
load_dotenv(dotenv_path=ENV_PATH)

# Get Values from ENV
API_KEY_LTA = os.getenv("API_KEY_LTA")
TIMING_URL = os.getenv("API_BUS_ARRIVAL_URL")
BUS_STOP_URL = os.getenv("API_BUS_STOP_URL")
ENV_LIST = [API_KEY_LTA, TIMING_URL, BUS_STOP_URL]

user_input = 0
bus_mem = ""
quit_refresh = ""
svc_mem = ""

while True:
    if bus_mem == "":
        user_input_str = input(
            """Bus Stop Arrival Timings
1. 77009
2. 77011
3. 77191
4. 65191
5. 65199
Q. Quit

For all other bus stops, please enter the 5-digit code.

Option/Code: 
"""
        )

        bus_svc_list_str = input(
            """Explicit Services View

Enter the explicit bus services to see only. Otherwise leave as blank to see all services.
i.e.: 5, 12e, 46

Services: 
"""
        )

        if bus_svc_list_str == "":
            bus_svc_list = []
            svc_mem = []

        else:
            bus_svc_list = bus_svc_list_str.split(",")

            for i in range(len(bus_svc_list)):
                bus_svc_list[i] = bus_svc_list[i].strip()

            svc_mem = bus_svc_list

        # Formulate Header

        # Custom Bus Stop
        if len(user_input_str) == 5:
            bus_stop_code = user_input_str
            bus_mem = user_input_str
            header_check = request_bus_stop_name_lta(bus_stop_code, API_KEY_LTA, BUS_STOP_URL)
            fallback_header = not header_check[2]
            request_bus_stop_timing(bus_stop_code, API_KEY_LTA, TIMING_URL, bus_svc_list, fallback_header)

        # Key Bus Stops
        elif user_input_str.isdigit() and int(user_input_str) <= len(KEY_BUS_STOPS):
            user_input = eval(user_input_str)
            bus_stop_code = KEY_BUS_STOPS[user_input - 1]
            bus_mem = KEY_BUS_STOPS[user_input - 1]
            header_check = request_bus_stop_name_lta(bus_stop_code, API_KEY_LTA, BUS_STOP_URL)
            fallback_header = not header_check[2]
            request_bus_stop_timing(bus_stop_code, API_KEY_LTA, TIMING_URL, bus_svc_list, fallback_header)

        # Quit
        elif user_input_str.isalpha() and user_input_str.lower() == "q":
            print("Exiting...")
            exit()

        # Unknown Value
        else:
            print("Unknown variable, please try again.")

    else:
        header_check = request_bus_stop_name_lta(bus_mem, API_KEY_LTA, BUS_STOP_URL)
        fallback_header = not header_check[2]
        request_bus_stop_timing(bus_mem, API_KEY_LTA, TIMING_URL, svc_mem, fallback_header)

    quit_refresh = ""
    while quit_refresh != "q" and quit_refresh != "r":
        quit_refresh = input(
            "Do you want to quit, refresh or query for a new bus stop? (Q to quit, R to Refresh, N for new bus): ")

        if quit_refresh.lower() == "q":
            print("Exiting...")
            exit()
        elif quit_refresh.lower() == "r":
            pass
        elif quit_refresh.lower() == "n":
            bus_mem = ""
            break
        else:
            print("Unknown value. Please try again.")
