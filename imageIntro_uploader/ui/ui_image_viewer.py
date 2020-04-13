#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  :   xiyu-mxx
@Contact :   ma138078@163.com
@File    :   ui_image_viewer.py
@Time    :   2020/4/5 3:57
@Desc    :
"""
import os
import sys
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QSplitter, QApplication, QHBoxLayout, QGroupBox, QLabel, QVBoxLayout, QWidget, \
    QSizePolicy, QFileDialog, qApp, QDesktopWidget, QPushButton


class ImageConverter(QMainWindow):
    """
    image converter window
    """

    def __init__(self, parent=None):
        super(ImageConverter, self).__init__(parent)
        self.cwd = os.getcwd()
        self.root = ''
        self.open_img_list = {}  # key: abs_path; value: 1/0 current display
        self._init_menu()
        self._init_ui()

    def _init_menu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('文件')
        self.editMenu = self.menu.addMenu('编辑')
        self.viewMenu = self.menu.addMenu('视图')
        self.toolMenu = self.menu.addMenu('工具')

        self.fileMenu.addAction('导入图片', self.slot_import_img, 'Ctrl+o')
        self.fileMenu.addAction('导出图片', self.slot_output_img, 'Ctrl+s')
        self.fileMenu.addAction('退出工具', qApp.quit, 'Ctrl+q')

    def _init_ui(self):
        vlay_main = QVBoxLayout()
        vlay_main.setSpacing(0)
        vlay_main.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setMinimumSize(1200, 800)

        self._init_tab()
        self._init_display()
        self._init_attr()
        vlay_main.addWidget(self.wg_tab)
        vlay_main.addWidget(self.splitter)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(vlay_main)
        self.setStyleSheet("background: white")

    def _init_tab(self):
        self.wg_tab = QWidget()
        self.wg_tab.setFixedHeight(30)
        self.wg_tab.setStyleSheet("background: #F3F3F3")
        hlay_tab = QHBoxLayout(self.wg_tab)
        hlay_tab.addStretch(1)
        hlay_tab.setContentsMargins(0, 0, 0, 0)

    def slot_import_img(self):
        if self.root != '':
            self.cwd = self.root
        file_path, file_type = QFileDialog.getOpenFileName(self, '选择图片', self.cwd, '*.jpg;*.jpeg;*.png;*.bmp;')
        self.root = os.path.split(file_path)[0]
        if os.path.exists(file_path) and file_path not in self.open_img_list:
            if len(self.open_img_list) != 0:
                self.update_open_img()
            self.slot_open_image(file_path)
            self.slot_add_tab(os.path.basename(file_path), file_path)
            self.open_img_list[file_path] = 1

    def update_open_img(self):
        not_display_img = [path for path, is_visible in self.open_img_list.items() if is_visible == 1][0]
        self.open_img_list[not_display_img] = 0

    def slot_output_img(self):
        print('导出图片')

    def _init_display(self):
        self.wg_display = QWidget(self.splitter)
        vlay_display = QHBoxLayout()
        vlay_display.setSpacing(0)
        vlay_display.setContentsMargins(0, 0, 0, 0)
        self._init_tool_bar()
        vlay_display.addWidget(self.wg_tool_bar)

        self.label_shower = QLabel()
        self.label_shower.setMinimumSize(600, 600)
        self.label_shower.setStyleSheet("background: #3366CC")
        vlay_display.addWidget(self.label_shower)
        self.wg_display.setLayout(vlay_display)

    def _init_tool_bar(self):
        self.wg_tool_bar = QWidget()
        self.wg_tool_bar.setFixedWidth(30)
        self.wg_tool_bar.setStyleSheet("background: #FF6633")
        vlay_tool = QVBoxLayout(self.wg_tool_bar)
        vlay_tool.setContentsMargins(0, 0, 0, 0)

    def _init_attr(self):
        right_group_box = QGroupBox(self.splitter)
        right_group_box.setMinimumWidth(300)
        right_vlay = QVBoxLayout()
        right_group_box.setLayout(right_vlay)
        right_vlay.addWidget(QGroupBox('基本尺寸'))
        right_vlay.addWidget(QGroupBox('详细尺寸'))

    def slot_open_image(self, img_path):
        img = QImage(img_path)
        img_w, img_h = img.width(), img.height()
        painter_w, painter_h = self.label_shower.size().width(), self.label_shower.size().height()

        w_scale = h_scale = 1
        if img_w > painter_w:
            w_scale = painter_w / img_w
        if img_h > painter_h:
            h_scale = painter_h / img_h
        scale = min(w_scale, h_scale)

        scaleImg = QPixmap.fromImage(img.scaled(QSize(int(img_w * scale), int(img_h * scale))))
        self.label_shower.setPixmap(scaleImg)

    def slot_add_tab(self, img_name, abs_path):
        add_label = TabLabel(img_name, abs_path)
        add_label.closedSignal.connect(self.slot_del_tab)
        self.wg_tab.layout().insertWidget(0, add_label)

    def slot_del_tab(self, abs_path):
        if abs_path in self.open_img_list.keys():
            self.findChild(QWidget, abs_path).deleteLater()
            if self.open_img_list[abs_path] == 1:
                self.label_shower.clear()


class TabLabel(QWidget):
    """
    custom tab label: fixed size, with close button
    """
    closedSignal = pyqtSignal(str)

    def __init__(self, name, abs_path, parent=None):
        super(TabLabel, self).__init__(parent)
        self.tab_name = name.split('.')[0]
        self.abs_path = abs_path
        self.setObjectName(abs_path)
        self.resize(QSize(35, 30))
        self.setStyleSheet("background: #66CCFF; border: None; font:11pt 'Arial';")
        self._init_ui()

    def _init_ui(self):
        hlay_label = QHBoxLayout(self)
        hlay_label.setSpacing(10)
        hlay_label.setContentsMargins(0, 0, 0, 0)

        label_content = QLabel(self.tab_name)
        but_close = QPushButton()
        but_close.setFixedSize(QSize(30, 30))
        but_close.clicked.connect(self.slot_close_tab)
        but_close.setStyleSheet("border: None; border-image: url(../../res/image/close.png)")

        hlay_label.addSpacing(10)
        hlay_label.addWidget(label_content)
        hlay_label.addWidget(but_close)

    def slot_close_tab(self):
        self.closedSignal.emit(self.abs_path)


test_path = r'D:\Guilinbird\qunxing_tools\test_data'
def get_data():
    file_list = os.listdir(test_path)
    return file_list[0], os.path.join(test_path, file_list[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageConverter()
    # name, abs_path = get_data()
    win.show()
    sys.exit(app.exec_())
