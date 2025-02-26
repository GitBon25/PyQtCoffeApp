import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QDialog


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.coffee_id = coffee_id
        self.saveButton.clicked.connect(self.saveData)
        self.cancelButton.clicked.connect(self.reject)

        if self.coffee_id is not None:
            self.loadData()

    def loadData(self):
        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM coffee WHERE id=?",
                           (self.coffee_id,))
            row = cursor.fetchone()
            if row:
                self.nameEdit.setText(row[1])
                self.roastEdit.setText(row[2])
                self.formEdit.setText(row[3])
                self.tasteEdit.setText(row[4])
                self.priceEdit.setText(str(row[5]))
                self.volumeEdit.setText(str(row[6]))
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            conn.close()

    def saveData(self):
        name = self.nameEdit.text()
        roast = self.roastEdit.text()
        form = self.formEdit.text()
        taste = self.tasteEdit.text()
        price = self.priceEdit.text()
        volume = self.volumeEdit.text()

        if not name or not roast or not form or not taste or not price or not volume:
            QMessageBox.warning(
                self, "Ошибка", "Все поля должны быть заполнены")
            return

        conn = sqlite3.connect('coffee.sqlite')
        cursor = conn.cursor()
        try:
            if self.coffee_id is None:
                cursor.execute("INSERT INTO coffee (name, roast, form, taste, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
                               (name, roast, form, taste, price, volume))
            else:
                cursor.execute("UPDATE coffee SET name=?, roast=?, form=?, taste=?, price=?, volume=? WHERE id=?",
                               (name, roast, form, taste, price, volume, self.coffee_id))
            conn.commit()
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
        finally:
            conn.close()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.refreshButton.clicked.connect(self.loadData)
        self.addButton.clicked.connect(self.addCoffee)
        self.editButton.clicked.connect(self.editCoffee)
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

    def addCoffee(self):
        dialog = AddEditCoffeeForm(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.loadData()

    def editCoffee(self):
        selected_row = self.coffeeTable.currentRow()
        if selected_row == -1:
            QMessageBox.warning(
                self, "Ошибка", "Выберите запись для редактирования")
            return

        coffee_id = self.coffeeTable.item(selected_row, 0).text()
        dialog = AddEditCoffeeForm(self, coffee_id)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.loadData()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())
