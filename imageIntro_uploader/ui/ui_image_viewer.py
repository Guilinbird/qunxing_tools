#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   xiyu-mxx
@Contact :   ma138078@163.com
@File    :   ui_image_viewer.py
@Time    :   2020/4/5 3:57
@Desc    :
'''
import os
import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QSplitter, QApplication, QHBoxLayout, QGroupBox, QLabel, QVBoxLayout, QWidget, \
    QSizePolicy, QFileDialog, qApp


class ImageConverter(QMainWindow):
    """
    image converter window
    """

    def __init__(self, parent=None):
        super(ImageConverter, self).__init__(parent)
        self.cwd = os.getcwd()
        self.root = ''
        self._initMenu()
        self._initUI()

    def _initMenu(self):
        self.menu = self.menuBar()
        self.fileMenu = self.menu.addMenu('文件')
        self.editMenu = self.menu.addMenu('编辑')
        self.viewMenu = self.menu.addMenu('视图')
        self.toolMenu = self.menu.addMenu('工具')

        # self.fileMenu.addAction('导入图片', self.slotImportImg, Qt.CTRL+Qt.Key_I)
        self.fileMenu.addAction('导入图片', self.slotImportImg, 'Ctrl+i')
        self.fileMenu.addAction('导出图片', self.slotOutputImg, 'Ctrl+o')
        self.fileMenu.addAction('退出工具', qApp.quit, 'Ctrl+q')

    def _initUI(self):
        vlayMain = QVBoxLayout()
        vlayMain.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setMinimumSize(1200, 800)

        self._initTab()
        self._initDisplay()
        self._initAttr()
        vlayMain.addWidget(self.wgTab)
        vlayMain.addWidget(self.splitter)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(vlayMain)

    def _initTab(self):
        self.wgTab = QWidget()
        self.wgTab.setFixedHeight(20)
        self.wgTab.setStyleSheet("background: #99FF99")
        hlayTab = QHBoxLayout(self.wgTab)
        hlayTab.setContentsMargins(0, 0, 0, 0)

    def slotImportImg(self):
        if self.root != '':
            self.cwd = self.root
        path, type = QFileDialog.getOpenFileName(self, '选择图片', self.cwd, '*.jpg;*.png;*.bmp')
        self.root = os.path.split(path)[0]
        if os.path.exists(path):
            self.slotOpenImage(path)

    def slotOutputImg(self):
        print('导出图片')

    def _initDisplay(self):
        self.wgDisplay = QWidget(self.splitter)
        vlayDisplay = QHBoxLayout()
        vlayDisplay.setContentsMargins(0, 0, 0, 0)
        self._initToolBar()
        vlayDisplay.addWidget(self.wgToolBar)

        self.labelShower = QLabel()
        self.labelShower.setMinimumSize(600, 600)
        self.labelShower.setStyleSheet("background: #3366CC")
        vlayDisplay.addWidget(self.labelShower)
        self.wgDisplay.setLayout(vlayDisplay)

    def _initToolBar(self):
        self.wgToolBar = QWidget()
        self.wgToolBar.setFixedWidth(20)
        self.wgToolBar.setStyleSheet("background: #FF6633")
        vlayTool = QVBoxLayout(self.wgToolBar)
        vlayTool.setContentsMargins(0, 0, 0, 0)

    def _initAttr(self):
        rightGroupBox = QGroupBox(self.splitter)
        rightGroupBox.setMinimumWidth(300)
        rightvlay = QVBoxLayout()
        rightGroupBox.setLayout(rightvlay)
        rightvlay.addWidget(QGroupBox('基本尺寸'))
        rightvlay.addWidget(QGroupBox('详细尺寸'))

    def slotOpenImage(self, imgPath):
        img = QImage(imgPath)
        img_w, img_h = img.width(), img.height()
        painter_w, painter_h = self.labelShower.size().width(), self.labelShower.size().height()

        w_scale = h_scale = 1
        if img_w > painter_w:
            w_scale = painter_w / img_w
        if img_h > painter_h:
            h_scale = painter_h / img_h
        scale = min(w_scale, h_scale)

        scaleImg = QPixmap.fromImage(img.scaled(QSize(int(img_w * scale), int(img_h * scale)), Qt.IgnoreAspectRatio))
        self.labelShower.setPixmap(scaleImg)


class OpenImageCard(QLabel):
    """
    open image label
    """

    def __init__(self, imagePath):
        super(OpenImageCard, self).__init__()
        self.imagePath = imagePath
        self.checkPath()
        self.setAttr()

    def checkPath(self):
        if os.path.exists(self.imagePath) and os.path.splitext(self.imagePath)[1] in ['.jpg', '.png', '.bmp']:
            return

    def setAttr(self):
        self.setObjectName(self.imagePath)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ImageConverter()
    win.show()
    sys.exit(app.exec_())
