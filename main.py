from PyQt5.Qt import *
from magnet_search_ui import Ui_Form
from spider import MagnetSpider


class Window(QWidget, Ui_Form):
    def __init__(self, parent=None, *args, **kwargs):
        super(Window, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.magnets_list = []
        self.btn_connect()

    def btn_connect(self):
        self.pushButton.clicked.connect(self._show_result)
        self.pushButton_2.clicked.connect(self._clear)
        self.listWidget.doubleClicked.connect(self._open_magnet)

    def _show_result(self):
        input_info = self.lineEdit.text()
        url = 'https://findcl.com/list?q=' + input_info
        titles_list, magnets_list = MagnetSpider(url).run()
        self.magnets_list = magnets_list
        self.listWidget.clear()
        self.listWidget.addItems(titles_list)
        self.listWidget.setToolTip('双击使用迅雷下载')

    def _open_magnet(self):
        index = self.listWidget.currentRow()
        magnet_url = self.magnets_list[index]
        QDesktopServices.openUrl(QUrl(magnet_url))

    def _clear(self):
        self.listWidget.clear()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())