# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------
from PyQt4 import QtCore, QtGui
import shutil
import sys
import re
import os
import os.path

# ---------------------------------Форма-----------------------------------------

class boundary_form(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModal)

        global types_mas
        global new_tn_mas
        global mas

#--------------------------Функции связанные c выводом-----------------------------

        full_dir = parent.d

        file = open(full_dir+"/constant/polyMesh/boundary", 'r') 
        data = file.read()
        file.close()

        str_grid = QtGui.QGridLayout()
   
        str_frame = QtGui.QFrame()
        str_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        str_frame.setFrameShape(QtGui.QFrame.Panel)
        str_frame.setFrameShadow(QtGui.QFrame.Sunken)
        str_frame.setLayout(str_grid)
        
        str_vbox = QtGui.QVBoxLayout() 
        str_vbox.addWidget(str_frame)

        struct_reg = re.compile(r"\S*\n\s*(?=[{])")
        struct_mas = struct_reg.findall(data)

        type_reg = re.compile(r"type\s*\S*(?=[;])")
        type_mas = type_reg.findall(data)
        
        m = 0
        mas_type = []
        for variant in range(len(type_mas)):
            type_div = type_mas[m].split("            ")
            m = m + 1
            mas_type.append(type_div[1])

        i = 1
        mas = []
        for elem in range(len(struct_mas)-1):
            div = struct_mas[i].split("\n")
            i = i + 1
            mas.append(div[0])

        n = 0
        types_mas = []
        for j in range(len(mas)):
            type_lbl = QtGui.QLabel("type: ")
            
            type_name = QtGui.QComboBox()
            type_name.setFixedSize(120, 25)
            type_list = ["symmetryPlane", "empty", "wall", "patch"]
            type_name.addItems(type_list)
            
            type_grid = QtGui.QGridLayout()
            type_grid.addWidget(type_lbl, 0, 0)
            type_grid.addWidget(type_name, 0, 1)
        
            type_frame = QtGui.QFrame()
            type_frame.setFixedSize(180, 40)
            type_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
            type_frame.setLayout(type_grid)
            type_hbox = QtGui.QHBoxLayout()
            type_hbox.addWidget(type_frame)

            str_lbl = QtGui.QLabel(mas[j])
            str_grid.addWidget(str_lbl, j, 0, alignment=QtCore.Qt.AlignCenter)
            str_grid.addLayout(type_hbox, j, 1)
        
            for r in range(len(type_list)):
                if type_list[r] == mas_type[j]:
                    type_name.setCurrentIndex(r)
                    n = n + 1
                    types_mas.append(type_name)

# ------------------------Функции связанные с формой-----------------------------

        def on_btnCancel_clicked():
            self.clear_label = QtGui.QLabel()
            parent.ffw.setTitleBarWidget(self.clear_label)
            self.close()

        def on_btnSave_clicked():
            w = 0
            new_tn_mas = []
            for w in range(len(types_mas)):
                new_tn_mas.append(types_mas[w].currentText())
                w = w + 1

            file = open(full_dir+"/constant/polyMesh/boundary", 'r') 
            data = file.read()
            file.close()

            for p in range(len(new_tn_mas)):
                type_reg = re.compile(r"\n\s*"+mas[p]+r"\n\s*\{\n\s*type\s*\S*\n\s*inGroups\s*\S\(\S*\)\S")
                type_mas = type_reg.findall(data)
                tn_txt_add = "\n"+"    "+mas[p]+"\n"+"    "+"{"+"\n"+"        "+"type            "+new_tn_mas[p]+";"+"\n"+"        "+"inGroups        "+"1("+new_tn_mas[p]+");"
                data = data.replace(type_mas[0], tn_txt_add)

                file = open(full_dir+"/constant/polyMesh/boundary", 'w')  
                file.write(data)
                file.close()

            parent.item = QtGui.QListWidgetItem("Сохранен файл: boundary", parent.listWidget)
            parent.color = QtGui.QColor("green")
            parent.item.setTextColor(parent.color)
            parent.listWidget.addItem(parent.item)

  # ---------------------Кнопки-----------------------

        btnSave = QtGui.QPushButton("Сохранить")
        btnSave.setFixedSize(70, 25)
        btnSave.clicked.connect(on_btnSave_clicked)
        btnCancel = QtGui.QPushButton("Отмена")
        btnCancel.setFixedSize(70, 25)
        btnCancel.clicked.connect(on_btnCancel_clicked)
        buttons_hbox = QtGui.QHBoxLayout()
        buttons_hbox.addWidget(btnSave)
        buttons_hbox.addWidget(btnCancel)

# -------------------------Фрейм формы---------------------------

        bound_grid = QtGui.QGridLayout()
        bound_grid.addLayout(str_vbox, 0, 0, alignment=QtCore.Qt.AlignCenter)
        bound_grid.addLayout(buttons_hbox, 1, 0, alignment=QtCore.Qt.AlignCenter)
        bound_frame = QtGui.QFrame()
        bound_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        bound_frame.setLayout(bound_grid)
        bound_vbox = QtGui.QVBoxLayout() 
        bound_vbox.addWidget(bound_frame)

# --------------------Размещение на форме всех компонентов---------

        form_1 = QtGui.QFormLayout()
        form_1.addRow(bound_vbox)
        self.setLayout(form_1)
