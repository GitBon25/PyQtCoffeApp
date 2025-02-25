import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.refreshButton.clicked.connect(self.loadData)
        self.loadData()

    def loadData(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM coffee")
            rows = cursor.fetchall()
            self.coffeeTable.setRowCount(len(rows))
            for rowIndex, row in enumerate(rows):
                for colIndex, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.coffeeTable.setItem(rowIndex, colIndex, item)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
