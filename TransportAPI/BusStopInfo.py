import json
import os
import ssl
import urllib.request
from dotenv import load_dotenv
from pathlib import Path


def request_bus_stop_name_lta(bus_stop_code: int or str, API_KEY: str, API_URL: str):
    """
    Gets and returns the Bus Stop Information of the Bus Stop.

    This method makes use of the data limit to cycle and check through if the codes matches.
    :param bus_stop_code: 5-digit Bus Stop Code
    :param API_KEY: LTA API Key
    :param API_URL: LTA Bus Stop API URL
    :return: Tuple containing:
             [0] -> Description
             [1] -> Road Name
             [2] -> Acquisition Success (for use in fallback)
    """
    skip_val = 0
    while True:
        URL = f"{API_URL}?$skip={skip_val}"

        headers = {
            "AccountKey": API_KEY,
            "accept": "application/json"
        }

        REQUEST = urllib.request.Request(url=URL, method="GET", headers=headers)

        with urllib.request.urlopen(REQUEST) as response:
            json_dict = response.read().decode("utf-8")
            dict_data = json.loads(json_dict)

            for data in dict_data["value"]:
                if data["BusStopCode"] == str(bus_stop_code):
                    print(
                        f"=======================================================================================\n"
                        f"{data['Description']} @ {data['RoadName']} [{bus_stop_code}]\n"
                        f"======================================================================================="
                    )

                    return (
                        data["Description"],
                        data["RoadName"],
                        True
                    )

            if len(dict_data["value"]) < 500:
                return (
                    None,
                    None,
                    False
                )

            else:
                skip_val += 500


def request_bus_stop_name_tih(bus_stop_code: int or str, API_KEY: str, API_URL: str):
    """
    RECOMMENDED NOT FOR USE FOR SECURITY REASONS.

    This API on TIH gets the data of the Bus Stop Information by referencing with a bus stop code.
    However due to certification issues (which is bypassed), it is therefore not recommended to use it.
    :param bus_stop_code: The 5-digit Bus Stop Code
    :param API_KEY: TIH API Key
    :param API_URL: TIH Bus Stop URL
    :return: Tuple containing:
             [0] -> Description,
             [1] -> Road Name
    """
    URL = f"{API_URL}/{bus_stop_code}"

    headers = {
        "X-API-Key": API_KEY,
        "accept": "application/json"
    }

    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    REQUEST = urllib.request.Request(url=URL, headers=headers, method="GET")

    with urllib.request.urlopen(REQUEST, context=ssl_ctx) as response:
        json_dict = response.read().decode("utf-8")
        dict_data = json.loads(json_dict)
        return (
            dict_data["data"][0]["description"],
            dict_data["data"][0]["roadName"]
        )


if __name__ == "__main__":
    ENV_PATH = os.path.join(Path(__file__).resolve().parent.parent, "RefKey.env")

    # Load ENV
    load_dotenv(dotenv_path=ENV_PATH)

    # Get Values from ENV
    API_KEY_LTA = os.getenv("API_KEY_LTA")
    LTA_BUS_STOP_URL = os.getenv("API_BUS_STOP_URL")
    API_KEY_TIH = os.getenv("API_KEY_TIH")
    TIH_BUS_STOP_URL = os.getenv("API_BUS_STOP_TIH_URL")

    returner = request_bus_stop_name_lta(77009, API_KEY_LTA, LTA_BUS_STOP_URL)
    # returner = request_bus_stop_name_tih(77009, API_KEY_TIH, TIH_BUS_STOP_URL)

    print(f"{returner[0]} | {returner[1]}")
