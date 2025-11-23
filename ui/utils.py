
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

def clear_table(table_widget: QTableWidget):
    """
    Очищает содержимое QTableWidget.
    """
    table_widget.clearContents()
    for row in range(table_widget.rowCount()):
        for col in range(table_widget.columnCount()):
            table_widget.setItem(row, col, QTableWidgetItem(""))
