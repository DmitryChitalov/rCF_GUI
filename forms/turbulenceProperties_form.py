# -*- coding: utf-8 -*-
# -----------------------------Импорт модулей-----------------------------------

from PyQt4 import QtCore, QtGui
import shutil
import sys
import re
import os
import os.path

# -----------------------------------Форма--------------------------------------

class turbulenceProperties_form(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModal)

# ------------------------Функции связанные с формой-----------------------------
        def on_btnSave_clicked():
            sT_txt = sT_name.currentText()
       
            file = open(full_dir+"/constant/turbulenceProperties", 'r') 
            data = file.read()
            file.close()

            sT_reg = re.compile(r"simulationType\s*\S*(?=[;])")
            sT_mas = sT_reg.findall(data)
            sT_txt_add = "simulationType  "+sT_txt
            data = data.replace(sT_mas[0], sT_txt_add)

            file = open(full_dir+"/constant/turbulenceProperties", 'w')  
            file.write(data)
            file.close()

            parent.item = QtGui.QListWidgetItem("Сохранен файл: turbulenceProperties", parent.listWidget)
            parent.color = QtGui.QColor("green")
            parent.item.setTextColor(parent.color)
            parent.listWidget.addItem(parent.item)

        def on_btnCancel_clicked():
            self.clear_label = QtGui.QLabel()
            parent.ffw.setTitleBarWidget(self.clear_label)
            self.close()

# -------------------------------Разметка формы----------------------------------

        sT_lbl = QtGui.QLabel("simulationType: ")
        sT_name = QtGui.QComboBox()
        sT_name.setFixedSize(100, 25)
        sT_list = ["demo", "laminar"]
        sT_name.addItems(sT_list)
        sT_grid = QtGui.QGridLayout()
        sT_grid.addWidget(sT_lbl, 0, 0)
        sT_grid.addWidget(sT_name, 0, 1)
        sT_frame = QtGui.QFrame()
        sT_frame.setFixedSize(210, 40)
        sT_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        sT_frame.setLayout(sT_grid)
        sT_hbox = QtGui.QHBoxLayout()
        sT_hbox.addWidget(sT_frame)

        # ---------------------Кнопки сохранения и отмены-----------------------

        btnSave = QtGui.QPushButton("Сохранить")
        btnSave.setFixedSize(70, 25)
        btnSave.clicked.connect(on_btnSave_clicked)
        btnCancel = QtGui.QPushButton("Отмена")
        btnCancel.setFixedSize(70, 25)
        btnCancel.clicked.connect(on_btnCancel_clicked)
        buttons_hbox = QtGui.QHBoxLayout()
        buttons_hbox.addWidget(btnSave)
        buttons_hbox.addWidget(btnCancel)

        # --------------------Фрейм элементов управления------------------------

        turbProp_grid = QtGui.QGridLayout()
        turbProp_grid.addLayout(sT_hbox, 0, 0, alignment=QtCore.Qt.AlignCenter)
        turbProp_grid.addLayout(buttons_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)
        turbProp_frame = QtGui.QFrame()
        turbProp_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        turbProp_frame.setFrameShape(QtGui.QFrame.Panel)
        turbProp_frame.setFrameShadow(QtGui.QFrame.Sunken)
        turbProp_frame.setLayout(turbProp_grid)
        turbProp_vbox = QtGui.QVBoxLayout() 
        turbProp_vbox.addWidget(turbProp_frame)

# ---------------------Размещение на форме всех компонентов-------------------------

        form_1 = QtGui.QFormLayout()
        form_1.addRow(turbProp_vbox)
        self.setLayout(form_1)

# --------------------------Функции связанные c выводом-----------------------------
        full_dir = parent.d

        file = open(full_dir+"/constant/turbulenceProperties", 'r') 
        data = file.read()
        file.close()

        sT_reg = re.compile(r"simulationType\s*\S*(?=[;])")
        sT_mas = sT_reg.findall(data) 
        
        sT_name_div = sT_mas[0].split()
        sT_name_mas = sT_name.count()   
        for i in range(sT_name_mas):
            if sT_name.itemText(i) == sT_name_div[1]:
                sT_name.setCurrentIndex(i)

