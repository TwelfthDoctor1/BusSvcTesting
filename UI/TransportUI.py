import sys
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableWidget
from TransportAPI.BusArrival import request_bus_stop_timing
from TransportAPI.BusRoute import get_bus_svc_route
from TransportAPI.BusService import return_bus_svc_json, get_bus_svc_list, get_bus_svc_directions
from TransportAPI.BusStopInfo import request_bus_stop_name_lta, return_bus_stop_name_json
from UI.UI_TransportUI import Ui_TransportService


class TransportMenu(QMainWindow):
    def __init__(self, parser: list, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_TransportService()
        self.parser = parser
        self.svc_query_cache = ""

        # Setup UI
        self.ui.setupUi(self)

        # Lock Cells
        self.lockBusStopTableCells()
        self.lockBusRouteTableCells()

        # Setup Bus Svc List
        self.ui.BusSvcList.addItems(get_bus_svc_list())

    def parseBusStopNumber(self):
        bus_count = 0
        bus_stop_num = self.ui.BusStopNumber.text()
        svc_list_str = self.ui.ExplicitSvcList.text()

        if svc_list_str == "":
            bus_svc_list = []

        else:
            bus_svc_list = svc_list_str.split(",")

            for i in range(len(bus_svc_list)):
                bus_svc_list[i] = bus_svc_list[i].strip()

        # Request For Data

        header_check = request_bus_stop_name_lta(bus_stop_num, self.parser[0])
        fallback_header = not header_check[2]
        bus_stop_list = request_bus_stop_timing(
            bus_stop_num, self.parser[0], bus_svc_list, fallback_header)

        # Clear Table
        self.ui.BusStopTable.clear()

        # Create Table w Row & Columns
        bus_num = len(bus_stop_list)
        self.ui.BusStopTable.setRowCount(bus_num * 10)
        self.ui.BusStopTable.setColumnCount(5)

        if not fallback_header:
            self.ui.BusStopTable.setItem(0, 0, QTableWidgetItem(f"{header_check[0]} @ {header_check[1]}"))
            self.ui.BusStopTable.setItem(0, 1, QTableWidgetItem(f"[{bus_stop_num}]"))
        else:
            self.ui.BusStopTable.setItem(0, 0, QTableWidgetItem(f"Bus Services for: "))
            self.ui.BusStopTable.setItem(0, 1, QTableWidgetItem(f"{bus_stop_num}"))

        # Populate Table
        for bus in bus_stop_list:
            # Handle Row
            row_designation = [1, 2, 3, 4, 5, 6, 7, 8, 9]

            for i in range(bus_count):
                for j in range(len(row_designation)):
                    k = row_designation[j]
                    k += 10
                    row_designation[j] = k

            # Service Header
            self.ui.BusStopTable.setItem(row_designation[0], 0, QTableWidgetItem(f"Service [{bus[0]}]"))
            self.ui.BusStopTable.setItem(row_designation[0], 1, QTableWidgetItem(f"{bus[1]}"))

            svc_info_returner = return_bus_svc_json(bus[0], 1)

            if svc_info_returner[4] != bus[18] and svc_info_returner[5] != bus[19]:
                svc_info_returner = return_bus_svc_json(bus[0], 2)

            if svc_info_returner[7] is False:
                svc_info = f"{return_bus_stop_name_json(svc_info_returner[4])[0]} >>> " \
                           f"{return_bus_stop_name_json(svc_info_returner[5])[0]} " \
                           f"[{svc_info_returner[3]}]"

            elif svc_info_returner[7] is True:
                svc_info = f"Loop @ {svc_info_returner[6]} to " \
                           f"{return_bus_stop_name_json(svc_info_returner[5])[0]} " \
                           f"[{svc_info_returner[3]}]"

            else:
                svc_info = f"This service does not exist."

            self.ui.BusStopTable.setItem(row_designation[1], 0, QTableWidgetItem(svc_info))

            # Next Bus
            self.ui.BusStopTable.setItem(row_designation[3], 0, QTableWidgetItem(f"{bus[2]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 1, QTableWidgetItem(f"{bus[5]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 2, QTableWidgetItem(f"{bus[8]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 3, QTableWidgetItem(f"Visit: {bus[11]}"))

            # 2nd Bus
            self.ui.BusStopTable.setItem(row_designation[4], 0, QTableWidgetItem(f"{bus[3]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 1, QTableWidgetItem(f"{bus[6]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 2, QTableWidgetItem(f"{bus[9]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 3, QTableWidgetItem(f"Visit: {bus[12]}"))

            # 3rd Bus
            self.ui.BusStopTable.setItem(row_designation[5], 0, QTableWidgetItem(f"{bus[4]}"))
            self.ui.BusStopTable.setItem(row_designation[5], 1, QTableWidgetItem(f"{bus[7]}"))
            self.ui.BusStopTable.setItem(row_designation[5], 2, QTableWidgetItem(f"{bus[10]}"))
            self.ui.BusStopTable.setItem(row_designation[5], 3, QTableWidgetItem(f"Visit: {bus[13]}"))

            # Estimated Time
            if bus[17] is True:
                self.ui.BusStopTable.setItem(row_designation[7], 0, QTableWidgetItem(f"Estimated Duration:"))
                self.ui.BusStopTable.setItem(row_designation[7], 1, QTableWidgetItem(f"{bus[14]} min"))
            else:
                self.ui.BusStopTable.setItem(row_designation[7], 0, QTableWidgetItem(f"Estimated Duration (Visit 1):"))
                self.ui.BusStopTable.setItem(row_designation[7], 1, QTableWidgetItem(f"{bus[15]} min"))
                self.ui.BusStopTable.setItem(row_designation[8], 0, QTableWidgetItem(f"Estimated Duration (Visit 2):"))
                self.ui.BusStopTable.setItem(row_designation[8], 1, QTableWidgetItem(f"{bus[16]} min"))

            bus_count += 1

        # Update Table
        self.updateBusArrTable()
        self.updateBusArrTable()

        self.ui.statusbar.showMessage("Bus Arrival Timing Data acquired & loaded.", 2000)

    def parseBusSvc(self):
        bus_svc = self.ui.BusSvcList.currentText()
        print(f"DEBUG: BUS_SVC {bus_svc} CACHE {self.svc_query_cache}")
        if bus_svc != "" and bus_svc != self.svc_query_cache:
            svc_json = get_bus_svc_directions(bus_svc)
            svc_list = []

            for svc in svc_json:
                if svc[6] is True:
                    svc_list.append(f"[{svc[1]}]: Loop @ {svc[5]}")
                else:
                    svc_list.append(f"[{svc[1]}]: {return_bus_stop_name_json(svc[3])[0]} --> "
                                    f"{return_bus_stop_name_json(svc[4])[0]}")

            self.ui.SvcDirList.clear()
            self.ui.SvcDirList.addItems(svc_list)
            self.svc_query_cache = bus_svc

    def parseSvcQuery(self):
        svc_num = self.ui.BusSvcList.currentText()

        if self.ui.SvcDirList.currentText() != "":
            svc_dir = self.ui.SvcDirList.currentText()[1]
        else:
            return

        svc_info = ''

        svc_info_route = get_bus_svc_directions(svc_num)
        svc_route = get_bus_svc_route(svc_num, svc_dir)

        for svc in svc_info_route:
            if svc[6] is True:
                svc_info = f"[{svc[1]}]: Loop @ {svc[5]}"
            else:
                print(f"DEBUG: SVC {svc[1]} {type(svc[1])} | {svc_dir} {type(svc_dir)}")
                if str(svc[1]) != svc_dir:
                    continue
                else:
                    svc_info = f"[{svc[1]}]: {return_bus_stop_name_json(svc[3])[0]} --> {return_bus_stop_name_json(svc[4])[0]}"

        print(f"[{svc_num}]: {svc_info}")

        route_len = len(svc_route)
        self.ui.BusSvcTable.setRowCount(route_len + 2)
        self.ui.BusSvcTable.setColumnCount(3)

        self.ui.BusSvcTable.setItem(0, 0, QTableWidgetItem(f"[{svc_num}]"))
        self.ui.BusSvcTable.setItem(0, 1, QTableWidgetItem(svc_info))

        print(svc_route)
        svc_route_bypass = 0

        for i in range(route_len):
            print(f"DEBUG: SVC Route {i + 1} | BYPASS : {svc_route_bypass} | IF I + 1 in LIST: {str(i + 1) in svc_route}")
            if str(i + 1) not in svc_route:
                svc_route_bypass += 1

                # self.ui.BusSvcTable.setItem(i + 2 - svc_route_bypass, 0, QTableWidgetItem(f'{i + 1 - svc_route_bypass}.'))
                # self.ui.BusSvcTable.setItem(i + 2 - svc_route_bypass, 1, QTableWidgetItem(f"NO DATA"))
                # self.ui.BusSvcTable.setItem(i + 2 - svc_route_bypass, 2, QTableWidgetItem(f"X KM"))

                continue

            print(f"{i + 1 - svc_route_bypass}. {return_bus_stop_name_json(svc_route[str(i + 1)][0])[0]} | {svc_route[str(i + 1)][1]} KM")
            self.ui.BusSvcTable.setItem(i + 2 - svc_route_bypass, 0, QTableWidgetItem(f'{i + 1 - svc_route_bypass}.'))
            self.ui.BusSvcTable.setItem(i + 2 - svc_route_bypass, 1, QTableWidgetItem(return_bus_stop_name_json(svc_route[str(i + 1)][0])[0]))
            self.ui.BusSvcTable.setItem(i + 2 - svc_route_bypass, 2, QTableWidgetItem(f"{svc_route[str(i + 1)][1]} KM"))

        self.updateBusRouteTable()
        self.updateBusRouteTable()

        self.ui.statusbar.showMessage("Bus Route Data acquired & loaded.", 2000)

    def resizeEvent(self, a0: QResizeEvent):
        self.ui.BusStopTable.update()
        self.ui.BusStopTable.resizeRowsToContents()
        self.ui.BusStopTable.resizeColumnsToContents()
        self.ui.BusSvcTable.update()
        self.ui.BusSvcTable.resizeRowsToContents()
        self.ui.BusSvcTable.resizeColumnsToContents()
        QMainWindow.resizeEvent(self, a0)

    def lockBusStopTableCells(self):
        self.ui.BusStopTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def lockBusRouteTableCells(self):
        self.ui.BusSvcTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def updateBusArrTable(self):
        self.ui.BusStopTable.update()
        self.ui.BusStopTable.resizeRowsToContents()
        self.ui.BusStopTable.resizeColumnsToContents()
        self.lockBusStopTableCells()

    def updateBusRouteTable(self):
        self.ui.BusSvcTable.update()
        self.ui.BusSvcTable.resizeRowsToContents()
        self.ui.BusSvcTable.resizeColumnsToContents()
        self.lockBusRouteTableCells()


def parse_to_ui(parser: list):
    app = QApplication(sys.argv)
    window = TransportMenu(parser=parser)
    window.show()
    app.exec()
