import sys
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableWidget
from TransportAPI.BusStop import request_bus_stop_timing
from UI.UI_TransportUI import Ui_TransportService


class TransportMenu(QMainWindow):
    def __init__(self, parser: list, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_TransportService()
        self.parser = parser

        # Setup UI
        self.ui.setupUi(self)

        # Lock Cells
        self.lockCells()

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
        bus_stop_list = request_bus_stop_timing(bus_stop_num, self.parser[0], self.parser[1], bus_svc_list)

        # Clear Table
        self.ui.BusStopTable.clear()

        # Create Table w Row & Columns
        bus_num = len(bus_stop_list)
        self.ui.BusStopTable.setRowCount(bus_num * 9)
        self.ui.BusStopTable.setColumnCount(5)

        self.ui.BusStopTable.setItem(0, 0, QTableWidgetItem(f"Bus Services for: "))
        self.ui.BusStopTable.setItem(0, 1, QTableWidgetItem(f"{bus_stop_num}"))

        # Populate Table
        for bus in bus_stop_list:
            # Handle Row
            row_designation = [1, 2, 3, 4, 5, 6, 7, 8]

            for i in range(bus_count):
                for j in range(len(row_designation)):
                    k = row_designation[j]
                    k += 9
                    row_designation[j] = k

            # Service Header
            self.ui.BusStopTable.setItem(row_designation[0], 0, QTableWidgetItem(f"Service [{bus[0]}]"))
            self.ui.BusStopTable.setItem(row_designation[0], 1, QTableWidgetItem(f"{bus[1]}"))

            # Next Bus
            self.ui.BusStopTable.setItem(row_designation[2], 0, QTableWidgetItem(f"{bus[2]}"))
            self.ui.BusStopTable.setItem(row_designation[2], 1, QTableWidgetItem(f"{bus[5]}"))
            self.ui.BusStopTable.setItem(row_designation[2], 2, QTableWidgetItem(f"{bus[8]}"))
            self.ui.BusStopTable.setItem(row_designation[2], 3, QTableWidgetItem(f"Visit: {bus[11]}"))

            # 2nd Bus
            self.ui.BusStopTable.setItem(row_designation[3], 0, QTableWidgetItem(f"{bus[3]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 1, QTableWidgetItem(f"{bus[6]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 2, QTableWidgetItem(f"{bus[9]}"))
            self.ui.BusStopTable.setItem(row_designation[3], 3, QTableWidgetItem(f"Visit: {bus[12]}"))

            # 3rd Bus
            self.ui.BusStopTable.setItem(row_designation[4], 0, QTableWidgetItem(f"{bus[4]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 1, QTableWidgetItem(f"{bus[7]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 2, QTableWidgetItem(f"{bus[10]}"))
            self.ui.BusStopTable.setItem(row_designation[4], 3, QTableWidgetItem(f"Visit: {bus[13]}"))

            # Estimated Time
            if bus[17] is True:
                self.ui.BusStopTable.setItem(row_designation[6], 0, QTableWidgetItem(f"Estimated Duration:"))
                self.ui.BusStopTable.setItem(row_designation[6], 1, QTableWidgetItem(f"{bus[14]} mins"))
            else:
                self.ui.BusStopTable.setItem(row_designation[6], 0, QTableWidgetItem(f"Estimated Duration (Visit 1):"))
                self.ui.BusStopTable.setItem(row_designation[6], 1, QTableWidgetItem(f"{bus[15]} mins"))
                self.ui.BusStopTable.setItem(row_designation[7], 0, QTableWidgetItem(f"Estimated Duration (Visit 2):"))
                self.ui.BusStopTable.setItem(row_designation[7], 1, QTableWidgetItem(f"{bus[16]} mins"))

            bus_count += 1

        # Update Table
        self.updateTable()
        self.updateTable()

    def resizeEvent(self, a0: QResizeEvent):
        self.ui.BusStopTable.update()
        self.ui.BusStopTable.resizeRowsToContents()
        self.ui.BusStopTable.resizeColumnsToContents()
        QMainWindow.resizeEvent(self, a0)

    def lockCells(self):
        self.ui.BusStopTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def updateTable(self):
        self.ui.BusStopTable.update()
        self.ui.BusStopTable.resizeRowsToContents()
        self.ui.BusStopTable.resizeColumnsToContents()
        self.lockCells()


def parse_to_ui(parser: list):
    app = QApplication(sys.argv)
    window = TransportMenu(parser=parser)
    window.show()
    app.exec()
