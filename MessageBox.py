from PyQt5.QtWidgets import QMessageBox


class MessageBox():
    @staticmethod
    def show(msg,title='',btns=None):
        dialog = QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setText(msg)
        if btns is not None:
            for btn in btns:
                dialog.addButton(btn)
        return dialog.exec()