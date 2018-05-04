 # -*- coding: utf-8 -*-
 # -----------------------------Импорт модулей-----------------------------------
 
from PyQt4 import QtCore, QtGui
import shutil
import sys
import re
import os
import os.path

# -----------------------------------Форма--------------------------------------

class refineMeshDict_form(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModal)

# ------------------------Функции связанные с формой-----------------------------

        def on_btnSave_clicked():
            set_txt = set_edit.text()
            cS_txt = cS_edit.currentText()
            t1_txt = t1_edit.text()
            t2_txt = t2_edit.text()
            p_txt = p_edit.currentText()
            t3_txt = t3_edit.text()
            d_txt = d_edit.text()
            uHT_txt = uHT_edit.currentText()
            gC_txt = gC_edit.currentText()
            wM_txt = wM_edit.currentText()

            file = open(full_dir+"/system/refineMeshDict", 'r') 
            data = file.read()
            file.close()

            set_reg = re.compile(r"set\s*\S*(?=[;])")
            set_mas = set_reg.findall(data)
            set_txt_add = "set             "+set_txt
            data = data.replace(set_mas[0], set_txt_add)

            cS_reg = re.compile(r"coordinateSystem\s\S*(?=[;])")
            cS_mas = cS_reg.findall(data)
            cS_txt_add = "coordinateSystem "+cS_txt
            data = data.replace(cS_mas[0], cS_txt_add)

            gC_reg = re.compile(r"globalCoeffs\n\{\n\s*\S*\s*\(\s\d\s\d\s\d\s\)\;\n\s*\S*\s*\(\s\d\s\d\s\d\s\)\;\n\}")
            gC_mas = gC_reg.findall(data)
            gC_txt_add = "globalCoeffs"+"\n"+"{"+"\n"+"    "+"tan1"+"            "+"("+t1_txt+");"+"\n"+"    "+"tan2"+"            "+"("+t2_txt+");"+"\n"+"}"
            data = data.replace(gC_mas[0], gC_txt_add)

            pLC_reg = re.compile(r"patchLocalCoeffs\n\{\n\s*\S*\s*\S*\;\n\s*\S*\s*\(\s\d\s\d\s\d\s\)\;\n\}")
            pLC_mas = pLC_reg.findall(data)
            pLC_txt_add = "patchLocalCoeffs"+"\n"+"{"+"\n"+"    "+"patch"+"           "+p_txt+";"+"\n"+"    "+"tan1"+"            "+"("+t3_txt+");"+"\n"+"}"
            data = data.replace(pLC_mas[0], pLC_txt_add)

            d_reg = re.compile(r"directions\s*\(\s\S*\s\)(?=[;])")
            d_mas = d_reg.findall(data)
            d_txt_add = "directions"+"      "+"( "+d_txt+" )"
            data = data.replace(d_mas[0], d_txt_add)

            uHT_reg = re.compile(r"useHexTopology\s*\S*(?=[;])")
            uHT_mas = uHT_reg.findall(data)
            uHT_txt_add = "useHexTopology  "+uHT_txt
            data = data.replace(uHT_mas[0], uHT_txt_add)

            gC_reg = re.compile(r"geometricCut\s*\S*(?=[;])")
            gC_mas = gC_reg.findall(data)
            gC_txt_add = "geometricCut    "+gC_txt
            data = data.replace(gC_mas[0], gC_txt_add)

            wM_reg = re.compile(r"writeMesh\s*\S*(?=[;])")
            wM_mas = wM_reg.findall(data)
            wM_txt_add = "writeMesh       "+wM_txt
            data = data.replace(wM_mas[0], wM_txt_add)

            file = open(full_dir+"/system/refineMeshDict", 'w')  
            file.write(data)
            file.close()

            parent.item = QtGui.QListWidgetItem("Сохранен файл: refineMeshDict", parent.listWidget)
            parent.color = QtGui.QColor("green")
            parent.item.setTextColor(parent.color)
            parent.listWidget.addItem(parent.item)

        def on_btnCancel_clicked():
            self.clear_label = QtGui.QLabel()
            parent.ffw.setTitleBarWidget(self.clear_label)
            self.close()

# -------------------------------Разметка формы----------------------------------
        # ------------------Верхний блок--------------------

        set_lbl = QtGui.QLabel("set: ")
        set_edit = QtGui.QLineEdit()
        set_edit.setFixedSize(80, 25)
        set_valid = QtGui.QRegExpValidator(QtCore.QRegExp("\S*"))
        set_edit.setValidator(set_valid)
        cS_lbl = QtGui.QLabel("coordinateSystem: ")
        cS_edit = QtGui.QComboBox()
        cS_edit.setFixedSize(80, 25)
        cS_list = ["demo", "global"]
        cS_edit.addItems(cS_list)
        tB_grid = QtGui.QGridLayout()
        tB_grid.addWidget(set_lbl, 0, 0, alignment=QtCore.Qt.AlignRight)
        tB_grid.addWidget(set_edit, 0, 1)
        tB_grid.addWidget(cS_lbl, 1, 0, alignment=QtCore.Qt.AlignRight)
        tB_grid.addWidget(cS_edit, 1, 1)
        tB_frame = QtGui.QFrame()
        tB_frame.setFixedSize(200, 60)
        tB_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        tB_frame.setLayout(tB_grid)
        tB_hbox = QtGui.QHBoxLayout() 
        tB_hbox.addWidget(tB_frame)

        # ---------------------Левый блок---------------------
        
        gC_lbl = QtGui.QLabel("globalCoeffs:")
        gC_lbl.setStyleSheet("qproperty-alignment: AlignCenter;")
        t1_lbl = QtGui.QLabel("tan1: ")
        t1_edit = QtGui.QLineEdit()
        t1_edit.setFixedSize(80, 25)
        t1_edit.setInputMask(" 9 9 9 ;_")
        t2_lbl = QtGui.QLabel("tan2: ")
        t2_edit = QtGui.QLineEdit()
        t2_edit.setFixedSize(80, 25)
        t2_edit.setInputMask(" 9 9 9 ;_")
        lB_grid = QtGui.QGridLayout()
        lB_grid.addWidget(t1_lbl, 0, 0)
        lB_grid.addWidget(t1_edit, 0, 1)
        lB_grid.addWidget(t2_lbl, 1, 0)
        lB_grid.addWidget(t2_edit, 1, 1)
        lB_frame = QtGui.QFrame()
        lB_frame.setFixedSize(130, 70)
        lB_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        lB_frame.setLayout(lB_grid)

        # ---------------------Правый блок---------------------
        
        pLC_lbl = QtGui.QLabel("patchLocalCoeffs:")
        pLC_lbl.setStyleSheet("qproperty-alignment: AlignCenter;")
        p_lbl = QtGui.QLabel("patch: ")
        p_edit = QtGui.QComboBox()
        p_edit.setFixedSize(80, 25)
        p_list = ["demo", "outside"]
        p_edit.addItems(p_list)
        t3_lbl = QtGui.QLabel("tan1: ")
        t3_edit = QtGui.QLineEdit()
        t3_edit.setFixedSize(80, 25)
        t3_edit.setInputMask(" 9 9 9 ;_")
        rB_grid = QtGui.QGridLayout()
        rB_grid.addWidget(p_lbl, 0, 0)
        rB_grid.addWidget(p_edit, 0, 1)
        rB_grid.addWidget(t3_lbl, 1, 0)
        rB_grid.addWidget(t3_edit, 1, 1)
        rB_frame = QtGui.QFrame()
        rB_frame.setFixedSize(130, 70)
        rB_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        rB_frame.setLayout(rB_grid)

        # -------------Боксы "правый + левый"-----------
        b_lbl_hbox = QtGui.QHBoxLayout()
        b_lbl_hbox.addWidget(gC_lbl)
        b_lbl_hbox.addWidget(pLC_lbl)
        b_hbox = QtGui.QHBoxLayout()
        b_hbox.addWidget(lB_frame)
        b_hbox.addWidget(rB_frame)

        # ------------------Нижний блок--------------------

        d_lbl = QtGui.QLabel("directions: ")
        d_edit = QtGui.QLineEdit()
        d_edit.setFixedSize(80, 25)
        d_valid = QtGui.QRegExpValidator(QtCore.QRegExp("\S*"))
        d_edit.setValidator(d_valid)
        uHT_lbl = QtGui.QLabel("useHexTopology: ")
        uHT_edit = QtGui.QComboBox()
        uHT_edit.setFixedSize(80, 25)
        uHT_list = ["demo", "no"]
        uHT_edit.addItems(uHT_list)
        gC_lbl = QtGui.QLabel("geometricCut: ")
        gC_edit = QtGui.QComboBox()
        gC_edit.setFixedSize(80, 25)
        gC_list = ["demo", "yes"]
        gC_edit.addItems(gC_list)
        wM_lbl = QtGui.QLabel("writeMesh: ")
        wM_edit = QtGui.QComboBox()
        wM_edit.setFixedSize(80, 25)
        wM_list = ["demo", "no"]
        wM_edit.addItems(wM_list)
        dB_grid = QtGui.QGridLayout()
        dB_grid.addWidget(d_lbl, 0, 0, alignment=QtCore.Qt.AlignRight)
        dB_grid.addWidget(d_edit, 0, 1)
        dB_grid.addWidget(uHT_lbl, 1, 0, alignment=QtCore.Qt.AlignRight)
        dB_grid.addWidget(uHT_edit, 1, 1)
        dB_grid.addWidget(gC_lbl, 2, 0, alignment=QtCore.Qt.AlignRight)
        dB_grid.addWidget(gC_edit, 2, 1)
        dB_grid.addWidget(wM_lbl, 3, 0, alignment=QtCore.Qt.AlignRight)
        dB_grid.addWidget(wM_edit, 3, 1)
        dB_frame = QtGui.QFrame()
        dB_frame.setFixedSize(200, 120)
        dB_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        dB_frame.setLayout(dB_grid)
        dB_hbox = QtGui.QHBoxLayout() 
        dB_hbox.addWidget(dB_frame)
        
        # ----------------------Кнопки сохранения и отмены--------------------------

        btnSave = QtGui.QPushButton("Сохранить")
        btnSave.setFixedSize(70, 25)
        btnSave.clicked.connect(on_btnSave_clicked)
        btnCancel = QtGui.QPushButton("Отмена")
        btnCancel.setFixedSize(70, 25)
        btnCancel.clicked.connect(on_btnCancel_clicked)
        buttons_hbox = QtGui.QHBoxLayout()
        buttons_hbox.addWidget(btnSave)
        buttons_hbox.addWidget(btnCancel)

        # --------------------Фрейм элементов управления----------------------------

        fvSolution_grid = QtGui.QGridLayout()
        fvSolution_grid.addLayout(tB_hbox, 0, 0)
        fvSolution_grid.addLayout(b_lbl_hbox, 1, 0)
        fvSolution_grid.addLayout(b_hbox, 2, 0)
        fvSolution_grid.addLayout(dB_hbox, 3, 0)
        fvSolution_grid.addLayout(buttons_hbox, 4, 0, alignment=QtCore.Qt.AlignCenter)
        fvSolution_frame = QtGui.QFrame()
        fvSolution_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        fvSolution_frame.setFrameShape(QtGui.QFrame.Panel)
        fvSolution_frame.setFrameShadow(QtGui.QFrame.Sunken)
        fvSolution_frame.setLayout(fvSolution_grid)
        fvSolution_vbox = QtGui.QVBoxLayout() 
        fvSolution_vbox.addWidget(fvSolution_frame)

# ---------------------Размещение на форме всех компонентов-------------------------

        form_1 = QtGui.QFormLayout()
        form_1.addRow(fvSolution_vbox)
        self.setLayout(form_1)

# --------------------------Функции связанные c выводом-----------------------------
        full_dir = parent.d

        file = open(full_dir+"/system/refineMeshDict", 'r') 
        data = file.read()
        file.close()

        set_reg = re.compile(r"set\s*\S*(?=[;])")
        set_mas = set_reg.findall(data)
        set_div = set_mas[0].split("             ")
        set_edit.setText(set_div[1])

        cS_reg = re.compile(r"coordinateSystem\s\S*(?=[;])")
        cS_mas = cS_reg.findall(data)
        cS_div = cS_mas[0].split(" ")
        cS_edit_mas = cS_edit.count()   
        for i in range(cS_edit_mas):
            if cS_edit.itemText(i) == cS_div[1]:
                cS_edit.setCurrentIndex(i)

        tan_reg = re.compile(r"\d\s\d\s\d")
        tan_mas = tan_reg.findall(data)
        p0, p1, p2 = tan_mas
        t1_edit.setText(p0)
        t2_edit.setText(p1)
        t3_edit.setText(p2)

        p_reg = re.compile(r"patch\s*\S*(?=[;])")
        p_mas = p_reg.findall(data)
        p_div = p_mas[0].split("           ")
        p_edit_mas = p_edit.count()   
        for i in range(p_edit_mas):
            if p_edit.itemText(i) == p_div[1]:
                p_edit.setCurrentIndex(i)

        d_reg = re.compile(r"directions\s*\(\s\S*\s\)(?=[;])")
        d_mas = d_reg.findall(data)
        d_div = d_mas[0].split("      ")
        d_div_mas = d_div[1].split(" ")
        d_edit.setText(d_div_mas[1])

        uHT_reg = re.compile(r"useHexTopology\s*\S*(?=[;])")
        uHT_mas = uHT_reg.findall(data)
        uHT_div = uHT_mas[0].split("  ")
        uHT_edit_mas = uHT_edit.count()   
        for i in range(uHT_edit_mas):
            if uHT_edit.itemText(i) == uHT_div[1]:
                uHT_edit.setCurrentIndex(i)

        gC_reg = re.compile(r"geometricCut\s*\S*(?=[;])")
        gC_mas = gC_reg.findall(data)
        gC_div = gC_mas[0].split("    ")
        gC_edit_mas = gC_edit.count()   
        for i in range(gC_edit_mas):
            if gC_edit.itemText(i) == gC_div[1]:
                gC_edit.setCurrentIndex(i)

        wM_reg = re.compile(r"writeMesh\s*\S*(?=[;])")
        wM_mas = wM_reg.findall(data)
        wM_div = wM_mas[0].split("       ")
        wM_edit_mas = wM_edit.count()   
        for i in range(wM_edit_mas):
            if wM_edit.itemText(i) == wM_div[1]:
                wM_edit.setCurrentIndex(i)


