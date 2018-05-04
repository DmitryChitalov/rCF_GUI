# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------
from PyQt4 import QtCore, QtGui
import shutil
import sys
import re
import os
import os.path
import subprocess
import time
import getpass

# -----------Дочерний поток для запуска процесса генерации сетки-----------------

class MyThread(QtCore.QThread):
    def __init__(self, full_dir, parent=None):
        QtCore.QThread.__init__(self, parent)
        global fd
        fd = full_dir
    def run(self):
        global proc

        file = open(fd+"/out_mesh.log", "w")
        proc = subprocess.Popen(["bash "+fd+"/MESH_BASH"], cwd = fd, shell = True, stdout=file, stderr=file)
        while proc.poll() is None:
            time.sleep(0.5)

# -----------------------------Главный поток программы---------------------------------

class mesh_form(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.WindowModal)

        full_dir = parent.d
        self.t1 = MyThread(full_dir)

        # --------------------------Функции, связанные с формой-------------------------

        def fmtf_clicked():
            prs_frame.setStyleSheet("border-color: dimgray;")
            mesh_edit.setText("")
            prs_frame.setEnabled(True)
            
        def f3Dmtf_clicked():
            prs_frame.setStyleSheet("border-color: dimgray;")
            mesh_edit.setText("")
            prs_frame.setEnabled(True)
            
        def on_path_choose():
            global mesh_dir
            user = getpass.getuser()
            mesh_dir = QtGui.QFileDialog.getOpenFileName(directory="/home/"+user)
            mesh_reg = re.compile(r"\S*(?<=[\/])\S*msh")
            mesh_mas = mesh_reg.findall(mesh_dir)

            if mesh_mas != []:
                mesh_edit.setText(mesh_dir)
            else:
                dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                                           "Внимание!", "Это не сетка. Выберите другой файл",
                                           buttons = QtGui.QMessageBox.Ok)
                result = dialog.exec_()

        def on_started():
            parent.treeview.setEnabled(False)

        def on_finished():
            global mas

            if proc.returncode == 0:
                full_dir = parent.d

                file = open(full_dir+"/constant/polyMesh/boundary", 'r') 
                data = file.read()
                file.close()

                struct_reg = re.compile(r"\S*\n\s*(?=[{])")
                struct_mas = struct_reg.findall(data)

                i = 1
                mas = []
                for elem in range(len(struct_mas)-1):
                    div = struct_mas[i].split("\n")
                    i = i + 1
                    mas.append(div[0])

                file_U = open(full_dir+"/0/U", 'a')                 
                file_U.write("\n{\n")
                for el in range(len(mas)):
                    file_U.write("    " + mas[el] + "\n    {\n        type            empty;\n    }\n")
                file_U.write("}")
                file_U.close()

                file_T = open(full_dir+"/0/T", 'a')                 
                file_T.write("\n{\n")
                for el in range(len(mas)):
                    file_T.write("    " + mas[el] + "\n    {\n        type            empty;\n    }\n")
                file_T.write("}")
                file_T.close()
    
                file_p = open(full_dir+"/0/p", 'a')                 
                file_p.write("\n{\n")
                for el in range(len(mas)):
                    file_p.write("    " + mas[el] + "\n    {\n        type            empty;\n    }\n")
                file_p.write("}")
                file_p.close()
                
                parent.listWidget.clear()
                parent.item = QtGui.QListWidgetItem("Расчетная сетка успешно сгенерирована", parent.listWidget)
                parent.color = QtGui.QColor("green")
                parent.item.setTextColor(parent.color)
                parent.listWidget.addItem(parent.item)
            else:
                parent.item = QtGui.QListWidgetItem("Расчетная сетка не сгенерирована", parent.listWidget)
                parent.color = QtGui.QColor("red")
                parent.item.setTextColor(parent.color)
                parent.listWidget.addItem(parent.item)
            parent.treeview.setEnabled(True)

        def on_save_clicked():
            full_dir = parent.d
            f = open(full_dir+'/MESH_BASH', 'w')
            if fmtf_radio.isChecked():
                f.write('#!/bin/sh' + '\n' + '. /opt/openfoam231/etc/bashrc' + '\n' + 'fluentMeshToFoam ' + mesh_dir + '\n' + 'exit')
                f.close()

            elif f3Dmtf_radio.isChecked():
                f.write('#!/bin/sh' + '\n' + '. /opt/openfoam231/etc/bashrc' + '\n' + 'fluent3DMeshToFoam ' + mesh_dir + '\n' + 'exit')
                f.close()
                
            self.t1.start()
            shutil.copytree("./matches/0", full_dir + "/0")

        def on_cancel_clicked():
            self.clear_label = QtGui.QLabel()
            parent.ffw.setTitleBarWidget(self.clear_label)
            parent.treeview.setEnabled(False)
            self.close()

        self.connect(self.t1, QtCore.SIGNAL("finished()"), on_finished)
        self.connect(self.t1, QtCore.SIGNAL("started()"), on_started)

        fmtf_radio = QtGui.QRadioButton("Импорт 2D-сетки")
        fmtf_radio.toggled.connect(fmtf_clicked)

        f3Dmtf_radio = QtGui.QRadioButton("Импорт 3D-сетки")
        f3Dmtf_radio.toggled.connect(f3Dmtf_clicked)

# -------------------------Структура элементов управления----------------------------

        mesh_label = QtGui.QLabel("Путь: ")
        path_button = QtGui.QPushButton("...")
        path_button.clicked.connect(on_path_choose)
        path_button.setFixedSize(25, 25)
        mesh_edit = QtGui.QLineEdit()
        mesh_edit.setFixedSize(290, 25)

# -------------------Фрейм элементов управления---------------------

        prs_grid = QtGui.QGridLayout()
        prs_grid.addWidget(mesh_label, 0, 0)
        prs_grid.addWidget(path_button, 0, 1)
        prs_grid.addWidget(mesh_edit, 0, 2)
        prs_frame = QtGui.QFrame()
        prs_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        prs_frame.setLayout(prs_grid)
        prs_frame.setEnabled(False)
        prs_frame.setStyleSheet("border-color: darkgray;")

# ---------------------Кнопки сохранения и отмены и их блок-------------------------

        save_button = QtGui.QPushButton("Сохранить")
        save_button.setFixedSize(70, 25)
        save_button.clicked.connect(on_save_clicked)
        cancel_button = QtGui.QPushButton("Отмена")
        cancel_button.setFixedSize(70, 25)
        cancel_button.clicked.connect(on_cancel_clicked)
        buttons_hbox = QtGui.QHBoxLayout()
        buttons_hbox.addWidget(save_button)
        buttons_hbox.addWidget(cancel_button)

# -------------------------Фрейм формы---------------------------

        mesh_grid = QtGui.QGridLayout()
        mesh_grid.addWidget(fmtf_radio, 0, 0, alignment=QtCore.Qt.AlignCenter)
        mesh_grid.addWidget(f3Dmtf_radio, 1, 0, alignment=QtCore.Qt.AlignCenter)
        mesh_grid.addWidget(prs_frame, 2, 0, alignment=QtCore.Qt.AlignCenter)
        mesh_grid.addLayout(buttons_hbox, 3, 0, alignment=QtCore.Qt.AlignCenter)
        mesh_frame = QtGui.QFrame()
        mesh_frame.setStyleSheet(open("./styles/properties_form_style.qss","r").read())
        mesh_frame.setLayout(mesh_grid)
        mesh_vbox = QtGui.QVBoxLayout() 
        mesh_vbox.addWidget(mesh_frame)

# ---------------------Размещение на форме всех компонентов-------------------------

        form_1 = QtGui.QFormLayout()
        form_1.addRow(mesh_vbox)
        self.setLayout(form_1)
