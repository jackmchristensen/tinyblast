# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tinyblast_options.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QAbstractSpinBox, QApplication, QCheckBox,
    QComboBox, QDoubleSpinBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_TinyblastOptions(object):
    def setupUi(self, TinyblastOptions):
        if not TinyblastOptions.objectName():
            TinyblastOptions.setObjectName(u"TinyblastOptions")
        TinyblastOptions.resize(551, 432)
        self.actionSave_Settings = QAction(TinyblastOptions)
        self.actionSave_Settings.setObjectName(u"actionSave_Settings")
        self.actionReset_Settings = QAction(TinyblastOptions)
        self.actionReset_Settings.setObjectName(u"actionReset_Settings")
        self.actionHelp_on_Tinyblas_Options = QAction(TinyblastOptions)
        self.actionHelp_on_Tinyblas_Options.setObjectName(u"actionHelp_on_Tinyblas_Options")
        self.centralwidget = QWidget(TinyblastOptions)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Title = QLabel(self.centralwidget)
        self.Title.setObjectName(u"Title")
        font = QFont()
        font.setFamilies([u"Dubai"])
        font.setPointSize(28)
        font.setBold(True)
        self.Title.setFont(font)
        self.Title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.Title)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.Box)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Sunken)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 533, 296))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.filePathLabel = QLabel(self.scrollAreaWidgetContents)
        self.filePathLabel.setObjectName(u"filePathLabel")
        self.filePathLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.filePathLabel, 10, 0, 1, 1)

        self.qualitySlider = QSlider(self.scrollAreaWidgetContents)
        self.qualitySlider.setObjectName(u"qualitySlider")
        self.qualitySlider.setMaximum(100)
        self.qualitySlider.setSliderPosition(50)
        self.qualitySlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.qualitySlider, 2, 2, 1, 2)

        self.blankLabel = QLabel(self.scrollAreaWidgetContents)
        self.blankLabel.setObjectName(u"blankLabel")

        self.gridLayout.addWidget(self.blankLabel, 5, 3, 1, 1)

        self.line_01 = QFrame(self.scrollAreaWidgetContents)
        self.line_01.setObjectName(u"line_01")
        self.line_01.setFrameShape(QFrame.Shape.HLine)
        self.line_01.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_01, 8, 0, 1, 4)

        self.encodingLabel = QLabel(self.scrollAreaWidgetContents)
        self.encodingLabel.setObjectName(u"encodingLabel")
        self.encodingLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.encodingLabel, 1, 0, 1, 1)

        self.displaySizeComboBox = QComboBox(self.scrollAreaWidgetContents)
        self.displaySizeComboBox.addItem("")
        self.displaySizeComboBox.addItem("")
        self.displaySizeComboBox.setObjectName(u"displaySizeComboBox")
        self.displaySizeComboBox.setMinimumSize(QSize(170, 0))
        self.displaySizeComboBox.setMaximumSize(QSize(170, 16777215))

        self.gridLayout.addWidget(self.displaySizeComboBox, 4, 1, 1, 2)

        self.displaySizeLabel = QLabel(self.scrollAreaWidgetContents)
        self.displaySizeLabel.setObjectName(u"displaySizeLabel")
        self.displaySizeLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.displaySizeLabel, 4, 0, 1, 1)

        self.saveToFileCheckBox = QCheckBox(self.scrollAreaWidgetContents)
        self.saveToFileCheckBox.setObjectName(u"saveToFileCheckBox")
        self.saveToFileCheckBox.setChecked(True)
        self.saveToFileCheckBox.setTristate(False)

        self.gridLayout.addWidget(self.saveToFileCheckBox, 9, 1, 1, 1)

        self.filePathTextBox = QLineEdit(self.scrollAreaWidgetContents)
        self.filePathTextBox.setObjectName(u"filePathTextBox")

        self.gridLayout.addWidget(self.filePathTextBox, 10, 1, 1, 3)

        self.framePaddingSlider = QSlider(self.scrollAreaWidgetContents)
        self.framePaddingSlider.setObjectName(u"framePaddingSlider")
        self.framePaddingSlider.setMaximum(10)
        self.framePaddingSlider.setSliderPosition(4)
        self.framePaddingSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.framePaddingSlider, 7, 2, 1, 2)

        self.framePaddingLabel = QLabel(self.scrollAreaWidgetContents)
        self.framePaddingLabel.setObjectName(u"framePaddingLabel")
        self.framePaddingLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.framePaddingLabel, 7, 0, 1, 1)

        self.scaleSlider = QSlider(self.scrollAreaWidgetContents)
        self.scaleSlider.setObjectName(u"scaleSlider")
        self.scaleSlider.setMaximum(1000)
        self.scaleSlider.setValue(1000)
        self.scaleSlider.setSliderPosition(1000)
        self.scaleSlider.setOrientation(Qt.Orientation.Horizontal)

        self.gridLayout.addWidget(self.scaleSlider, 6, 2, 1, 2)

        self.saveToFileLabel = QLabel(self.scrollAreaWidgetContents)
        self.saveToFileLabel.setObjectName(u"saveToFileLabel")
        self.saveToFileLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.saveToFileLabel, 9, 0, 1, 1)

        self.scaleLabel = QLabel(self.scrollAreaWidgetContents)
        self.scaleLabel.setObjectName(u"scaleLabel")
        self.scaleLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.scaleLabel, 6, 0, 1, 1)

        self.formattingLabel = QLabel(self.scrollAreaWidgetContents)
        self.formattingLabel.setObjectName(u"formattingLabel")
        self.formattingLabel.setMinimumSize(QSize(150, 0))
        self.formattingLabel.setMaximumSize(QSize(150, 16777215))
        self.formattingLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.formattingLabel, 0, 0, 1, 1)

        self.line_00 = QFrame(self.scrollAreaWidgetContents)
        self.line_00.setObjectName(u"line_00")
        self.line_00.setFrameShape(QFrame.Shape.HLine)
        self.line_00.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_00, 3, 0, 1, 4)

        self.qualityLabel = QLabel(self.scrollAreaWidgetContents)
        self.qualityLabel.setObjectName(u"qualityLabel")
        self.qualityLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.qualityLabel, 2, 0, 1, 1)

        self.scaleSpinBox = QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.scaleSpinBox.setObjectName(u"scaleSpinBox")
        self.scaleSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.scaleSpinBox.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.scaleSpinBox.setMaximum(1.000000000000000)
        self.scaleSpinBox.setValue(1.000000000000000)

        self.gridLayout.addWidget(self.scaleSpinBox, 6, 1, 1, 1)

        self.qualitySpinBox = QSpinBox(self.scrollAreaWidgetContents)
        self.qualitySpinBox.setObjectName(u"qualitySpinBox")
        self.qualitySpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.qualitySpinBox.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.qualitySpinBox.setMinimum(0)
        self.qualitySpinBox.setMaximum(100)
        self.qualitySpinBox.setValue(50)

        self.gridLayout.addWidget(self.qualitySpinBox, 2, 1, 1, 1)

        self.framePaddingSpinBox = QSpinBox(self.scrollAreaWidgetContents)
        self.framePaddingSpinBox.setObjectName(u"framePaddingSpinBox")
        self.framePaddingSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.framePaddingSpinBox.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.framePaddingSpinBox.setMaximum(10)
        self.framePaddingSpinBox.setValue(4)

        self.gridLayout.addWidget(self.framePaddingSpinBox, 7, 1, 1, 1)

        self.widthSpinBox = QSpinBox(self.scrollAreaWidgetContents)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        self.widthSpinBox.setEnabled(True)
        self.widthSpinBox.setMaximumSize(QSize(80, 16777215))
        self.widthSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.widthSpinBox.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.widthSpinBox.setMaximum(999999999)
        self.widthSpinBox.setValue(1920)

        self.gridLayout.addWidget(self.widthSpinBox, 5, 1, 1, 1)

        self.heightSpinBox = QSpinBox(self.scrollAreaWidgetContents)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setEnabled(True)
        self.heightSpinBox.setMaximumSize(QSize(80, 16777215))
        self.heightSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.heightSpinBox.setMaximum(999999999)
        self.heightSpinBox.setValue(1080)

        self.gridLayout.addWidget(self.heightSpinBox, 5, 2, 1, 1)

        self.browseButton = QPushButton(self.scrollAreaWidgetContents)
        self.browseButton.setObjectName(u"browseButton")

        self.gridLayout.addWidget(self.browseButton, 11, 1, 1, 2)

        self.encodingComboBox = QComboBox(self.scrollAreaWidgetContents)
        self.encodingComboBox.addItem("")
        self.encodingComboBox.addItem("")
        self.encodingComboBox.addItem("")
        self.encodingComboBox.addItem("")
        self.encodingComboBox.addItem("")
        self.encodingComboBox.setObjectName(u"encodingComboBox")
        self.encodingComboBox.setMinimumSize(QSize(0, 0))
        self.encodingComboBox.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.encodingComboBox, 1, 1, 1, 2)

        self.formattingComboBox = QComboBox(self.scrollAreaWidgetContents)
        self.formattingComboBox.addItem("")
        self.formattingComboBox.addItem("")
        self.formattingComboBox.addItem("")
        self.formattingComboBox.addItem("")
        self.formattingComboBox.addItem("")
        self.formattingComboBox.setObjectName(u"formattingComboBox")
        self.formattingComboBox.setMinimumSize(QSize(0, 0))
        self.formattingComboBox.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.formattingComboBox, 0, 1, 1, 2)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.setObjectName(u"buttonsLayout")
        self.tinyblastButton = QPushButton(self.centralwidget)
        self.tinyblastButton.setObjectName(u"tinyblastButton")
        self.tinyblastButton.setMinimumSize(QSize(0, 30))

        self.buttonsLayout.addWidget(self.tinyblastButton)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setMinimumSize(QSize(0, 30))

        self.buttonsLayout.addWidget(self.applyButton)

        self.quitButton = QPushButton(self.centralwidget)
        self.quitButton.setObjectName(u"quitButton")
        self.quitButton.setMinimumSize(QSize(0, 30))

        self.buttonsLayout.addWidget(self.quitButton)


        self.verticalLayout.addLayout(self.buttonsLayout)

        TinyblastOptions.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(TinyblastOptions)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 551, 20))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        TinyblastOptions.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionSave_Settings)
        self.menuFile.addAction(self.actionReset_Settings)
        self.menuHelp.addAction(self.actionHelp_on_Tinyblas_Options)

        self.retranslateUi(TinyblastOptions)

        QMetaObject.connectSlotsByName(TinyblastOptions)
    # setupUi

    def retranslateUi(self, TinyblastOptions):
        TinyblastOptions.setWindowTitle(QCoreApplication.translate("TinyblastOptions", u"Tinyblast Options", None))
        self.actionSave_Settings.setText(QCoreApplication.translate("TinyblastOptions", u"(TODO) Save Settings", None))
        self.actionReset_Settings.setText(QCoreApplication.translate("TinyblastOptions", u"(TODO) Reset Settings", None))
        self.actionHelp_on_Tinyblas_Options.setText(QCoreApplication.translate("TinyblastOptions", u"(TODO) Help on Tinyblast Options", None))
        self.Title.setText(QCoreApplication.translate("TinyblastOptions", u"Tinyblast", None))
        self.filePathLabel.setText(QCoreApplication.translate("TinyblastOptions", u"File Path", None))
        self.blankLabel.setText("")
        self.encodingLabel.setText(QCoreApplication.translate("TinyblastOptions", u"Encoding", None))
        self.displaySizeComboBox.setItemText(0, QCoreApplication.translate("TinyblastOptions", u"Custom", None))
        self.displaySizeComboBox.setItemText(1, QCoreApplication.translate("TinyblastOptions", u"From Render Settings", None))

        self.displaySizeLabel.setText(QCoreApplication.translate("TinyblastOptions", u"Display Size", None))
        self.saveToFileCheckBox.setText("")
        self.framePaddingLabel.setText(QCoreApplication.translate("TinyblastOptions", u"Frame Padding", None))
        self.saveToFileLabel.setText(QCoreApplication.translate("TinyblastOptions", u"Save to File", None))
        self.scaleLabel.setText(QCoreApplication.translate("TinyblastOptions", u"Scale", None))
        self.formattingLabel.setText(QCoreApplication.translate("TinyblastOptions", u"Format", None))
        self.qualityLabel.setText(QCoreApplication.translate("TinyblastOptions", u"Quality", None))
        self.browseButton.setText(QCoreApplication.translate("TinyblastOptions", u"Browse...", None))
        self.encodingComboBox.setItemText(0, QCoreApplication.translate("TinyblastOptions", u"HEVC (H.265)", None))
        self.encodingComboBox.setItemText(1, QCoreApplication.translate("TinyblastOptions", u"H.264", None))
        self.encodingComboBox.setItemText(2, QCoreApplication.translate("TinyblastOptions", u"AV1", None))
        self.encodingComboBox.setItemText(3, QCoreApplication.translate("TinyblastOptions", u"MPEG-4", None))
        self.encodingComboBox.setItemText(4, QCoreApplication.translate("TinyblastOptions", u"VP9", None))

        self.formattingComboBox.setItemText(0, QCoreApplication.translate("TinyblastOptions", u"MP4", None))
        self.formattingComboBox.setItemText(1, QCoreApplication.translate("TinyblastOptions", u"MKV", None))
        self.formattingComboBox.setItemText(2, QCoreApplication.translate("TinyblastOptions", u"MOV", None))
        self.formattingComboBox.setItemText(3, QCoreApplication.translate("TinyblastOptions", u"AVI", None))
        self.formattingComboBox.setItemText(4, QCoreApplication.translate("TinyblastOptions", u"WebM", None))

#if QT_CONFIG(statustip)
        self.formattingComboBox.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.formattingComboBox.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.formattingComboBox.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.formattingComboBox.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.tinyblastButton.setText(QCoreApplication.translate("TinyblastOptions", u"Tinyblast", None))
        self.applyButton.setText(QCoreApplication.translate("TinyblastOptions", u"Apply", None))
        self.quitButton.setText(QCoreApplication.translate("TinyblastOptions", u"Quit", None))
        self.menuFile.setTitle(QCoreApplication.translate("TinyblastOptions", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("TinyblastOptions", u"Help", None))
    # retranslateUi

