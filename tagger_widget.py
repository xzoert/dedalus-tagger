# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tagger.ui'
#
# Created: Fri Nov  4 08:14:53 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 597)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/tagger/dedalus.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.leftWidget = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftWidget.sizePolicy().hasHeightForWidth())
        self.leftWidget.setSizePolicy(sizePolicy)
        self.leftWidget.setMinimumSize(QtCore.QSize(100, 0))
        self.leftWidget.setObjectName("leftWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.leftWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_6 = QtGui.QWidget(self.leftWidget)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.fileLabel = QtGui.QLabel(self.widget_6)
        self.fileLabel.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.fileLabel.setFont(font)
        self.fileLabel.setObjectName("fileLabel")
        self.horizontalLayout_5.addWidget(self.fileLabel)
        self.verticalLayout.addWidget(self.widget_6)
        self.resourceList = QtGui.QListWidget(self.leftWidget)
        self.resourceList.setObjectName("resourceList")
        self.verticalLayout.addWidget(self.resourceList)
        self.widget_4 = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(255)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QtCore.QSize(400, 0))
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtGui.QWidget(self.widget_4)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(0, 9, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.urlCaption = QtGui.QLabel(self.widget_2)
        self.urlCaption.setMinimumSize(QtCore.QSize(50, 0))
        self.urlCaption.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.urlCaption.setFont(font)
        self.urlCaption.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.urlCaption.setObjectName("urlCaption")
        self.horizontalLayout_2.addWidget(self.urlCaption)
        self.urlLabel = QtGui.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setItalic(True)
        self.urlLabel.setFont(font)
        self.urlLabel.setObjectName("urlLabel")
        self.horizontalLayout_2.addWidget(self.urlLabel)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_3 = QtGui.QWidget(self.widget_4)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setContentsMargins(0, 9, 0, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtGui.QLabel(self.widget_3)
        self.label_3.setMinimumSize(QtCore.QSize(50, 0))
        self.label_3.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.labelEdit = QtGui.QLineEdit(self.widget_3)
        self.labelEdit.setObjectName("labelEdit")
        self.horizontalLayout_3.addWidget(self.labelEdit)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.label_2 = QtGui.QLabel(self.widget_4)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tableView = QtGui.QTableView(self.widget_4)
        self.tableView.setObjectName("tableView")
        self.verticalLayout_2.addWidget(self.tableView)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget.setSizeIncrement(QtCore.QSize(0, 0))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setMinimumSize(QtCore.QSize(120, 40))
        self.cancelButton.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setWeight(75)
        font.setBold(True)
        self.cancelButton.setFont(font)
        self.cancelButton.setAutoFillBackground(False)
        self.cancelButton.setStyleSheet("")
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(self.widget)
        self.okButton.setMinimumSize(QtCore.QSize(50, 40))
        self.okButton.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setWeight(75)
        font.setBold(True)
        self.okButton.setFont(font)
        self.okButton.setAutoFillBackground(False)
        self.okButton.setStyleSheet("")
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Dedalus Tagger", None, QtGui.QApplication.UnicodeUTF8))
        self.fileLabel.setText(QtGui.QApplication.translate("MainWindow", "Files", None, QtGui.QApplication.UnicodeUTF8))
        self.urlCaption.setText(QtGui.QApplication.translate("MainWindow", "URL", None, QtGui.QApplication.UnicodeUTF8))
        self.urlLabel.setText(QtGui.QApplication.translate("MainWindow", "file:///questo/e/quello.pdf", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Label", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Tags", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("MainWindow", "Ok", None, QtGui.QApplication.UnicodeUTF8))

import tagger_rc
