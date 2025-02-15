import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit,
                             QHBoxLayout, QMenu, QAction,
                             QFileDialog, QMessageBox, QFontDialog,
                             QColorDialog)
from PyQt5.QtGui import QIcon, QColor, QFont

class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_widget = QTextEdit(self)

        self.initUI()
        self.createActions()
        self.createMenuBar()

    def initUI(self):
        self.setWindowTitle("Notepad")
        self.setGeometry(650, 250, 600, 500)
        self.setCentralWidget(self.text_widget)

        self.text_widget.setStyleSheet("padding-left: 5px;")

    def createMenuBar(self):
        menuBar = self.menuBar()

        file_menu = QMenu("File", self)
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.exit_action)

        style_menu = QMenu("Style", self)
        style_menu.addAction(self.font_action)
        style_menu.addAction(self.background_action)
        style_menu.addAction(self.reset_action)

        menuBar.addMenu(file_menu)
        menuBar.addMenu(style_menu)

        self.setStyleSheet("""
            QMenu, QMenuBar {
                font-size: 18px;
            }
        """)

        self.setMenuBar(menuBar)

    def createActions(self):
        self.new_action = QAction(QIcon("icons/new_icon.png"), "New", self, shortcut="Ctrl+N")
        self.open_action = QAction(QIcon("icons/open_icon.png"), "Open", self, shortcut="Ctrl+O")
        self.save_action = QAction(QIcon("icons/save_icon.png"), "Save", self, shortcut="Ctrl+S")
        self.exit_action = QAction(QIcon("icons/exit_icon.png"), "Exit", self, shortcut="Alt+F4")

        self.font_action = QAction(QIcon("icons/font-icon.png"), "Font", self, shortcut="Ctrl+F")
        self.background_action = QAction(QIcon("icons/background-icon.png"), "Background", self, shortcut="Ctrl+B")
        self.reset_action = QAction(QIcon("icons/reset_icon.png"), "Reset", self, shortcut="Ctrl+R")

        self.new_action.triggered.connect(self.new_file)
        self.save_action.triggered.connect(self.save_file)
        self.open_action.triggered.connect(self.open_file)
        self.exit_action.triggered.connect(self.close_program)

        self.font_action.triggered.connect(self.change_font)
        self.background_action.triggered.connect(self.change_background)
        self.reset_action.triggered.connect(self.reset_style)

    def new_file(self):
        if self.text_widget.toPlainText():
            msg = QMessageBox()
            ans = msg.question(self, "Create new file?", "You may not have saved your file", msg.Yes | msg.No)
            if ans == msg.Yes:
                self.text_widget.clear()

    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "C:/", "Text File (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_widget.toPlainText())

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "C:/", "Text File (*.txt)")
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.setText(content)

    def change_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.text_widget.setFont(font)

    def change_background(self):
        color = QColorDialog.getColor()
        self.text_widget.setStyleSheet(f"background-color: rgb{QColor.getRgb(color)}")

    def reset_style(self):
        msg = QMessageBox()
        ans = msg.question(self, "Reset all styles?", "You cannot undo this", msg.Yes | msg.No)
        if ans == msg.Yes:
            self.text_widget.setStyleSheet("background-color: white")
            self.text_widget.setFont(QFont( "Sans Serif,12,-1,5,50,0,0,0,0,0" ))

    def close_program(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = Notepad()
    notepad.show()
    sys.exit(app.exec_())