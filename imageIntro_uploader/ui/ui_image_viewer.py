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

import cv2
import numpy as np

from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QSplitter, QApplication, QHBoxLayout, QGroupBox, QLabel, QVBoxLayout, QWidget, \
    QFileDialog, qApp, QPushButton


class ImageConverter(QMainWindow):
    """
    image converter window
    """

    def __init__(self, parent=None):
        super(ImageConverter, self).__init__(parent)
        self.cwd = os.getcwd()
        self.root_path = os.path.join(os.path.expanduser("~"), 'Desktop')
        self.open_img_list = []
        self._init_menu()
        self._init_ui()
        self.setGeometry(200, 100, 1500, 900)

    def _init_menu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('文件')
        self.editMenu = self.menu.addMenu('编辑')
        self.viewMenu = self.menu.addMenu('视图')
        self.toolMenu = self.menu.addMenu('工具')

        self.fileMenu.addAction('打开图片', self.slot_open_img, 'Ctrl+o')
        self.fileMenu.addAction('保存图片', self.slot_save_img, 'Ctrl+s')
        self.fileMenu.addAction('退出工具', qApp.quit, 'Ctrl+q')

    def _init_ui(self):
        vlay_main = QVBoxLayout()
        vlay_main.setSpacing(0)
        vlay_main.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setMinimumSize(1200, 800)

        self._init_display()
        self._init_attr()
        vlay_main.addWidget(self.splitter)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(vlay_main)
        self.setStyleSheet("background: white")

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

    def slot_open_img(self):
        img_path = self.choose_img_file()
        if img_path and img_path not in self.open_img_list:
            np_img = self.read_img_2_np(img_path)

    def choose_img_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择图片', self.root_path, '*.jpg;*.jpeg;*.png;*.bmp;')
        if file_path:
            self.root_path = os.path.dirname(file_path)
            return file_path
        else:
            return False

    @staticmethod
    def read_img_2_np(img_path):
        for ch in img_path:
            if u'\u4e00' <= ch <= u'\u9fff':
                return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        return cv2.imread(img_path, -1)

    def slot_save_img(self):
        pass


class ImageTabWg(QWidget):

    def __init__(self, tab_name, img_array, parent=None):
        super(ImageTabWg, self).__init__(parent)
        self.tab_name = tab_name
        self.abs_path = img_array
        self.setObjectName(tab_name)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageConverter()
    win.show()
    sys.exit(app.exec_())
