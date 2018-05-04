# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------

from PyQt4 import QtCore, QtGui                                                 
import sys
import os
import subprocess
import re
import time
import getpass
import numpy as np
import sys
import os
import time
import threading
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pylab import *
import time
import pylab
import re
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib import animation
from add_classes.file_form_class import file_form_class
from add_classes.file_form_class import mesh_form_class
from forms.mesh_form import mesh_form

# ----------------Дочерний поток для останова процесса решения--------------------

class Vspom(QtCore.QThread):
    def __init__(self, full_dir, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        import signal

        vspom_file = open(full_dir+"/out_kill.log", "w")
        vspom_proc = subprocess.Popen(["bash "+full_dir+"/KILL_PROC_BASH"], cwd = full_dir, shell = True, stdout=vspom_file, stderr=vspom_file)
        while vspom_proc.poll() is None:
            time.sleep(0.5)

        if vspom_proc.returncode == 0:
            f_o = open(full_dir+"/out_kill.log", "r")
            data = f_o.read()
            f_o.close()

            con_reg = re.compile(r"\d*")
            con_mas = con_reg.findall(data)
            proc_to_kill = con_mas[0]

            os.kill(int(proc_to_kill), signal.SIGKILL)

# ----------------Дочерний поток для запуска процесса визуализации--------------------

class view_Thread(QtCore.QThread):
    def __init__(self, full_dir, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        global view
        view = subprocess.Popen(["bash "+full_dir+"/VIEW_BASH"], cwd = full_dir, shell = True)
        while view.poll() is None:
            time.sleep(0.5)

# -----------------------------Главный поток программы---------------------------------

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        global full_dir

        new_dir = "/home/kalina"
        prj_name = "Тестовый_пример"
        new_app = "rhoCentralFoam"

        full_dir = new_dir+"/"+prj_name
        self.d = full_dir

        self.t2 = Vspom(full_dir)
        self.t3 = view_Thread(full_dir)

        f = open(full_dir+'/SOLVER_BASH', 'w')
        f.write('#!/bin/sh' + '\n' + '. /opt/openfoam231/etc/bashrc' + '\n' + new_app + '\n' + 'exit')
        f.close()

        vspom = open(full_dir+'/KILL_PROC_BASH', 'w')
        vspom.write('#!/bin/sh' + '\n' + '. /opt/openfoam231/etc/bashrc' + '\n' + 'pidof ' + new_app + '\n' + 'exit')
        vspom.close()
        
        self.connect(self.t3, QtCore.SIGNAL("started()"), self.on_t3_started)

        # ...........................Функция открытия формы сетки...........................

        def on_mesh_open():
            mesh_form_class.mesh_form_class_func(self)
            mef = mesh_form_class.out_mesh_form_func()
            self.setCentralWidget(self.ffw)
            self.ffw.setTitleBarWidget(self.ffw_frame)
            self.ffw_label.setText("Форма импорта сетки")
            self.ffw_label.setStyleSheet("border-style: none;" "font-size: 8pt;")
            self.ffw.setWidget(mef)

        # ...........................Функция запуска первого потока...........................

        def on_task_open():
            global proc
            global kon_x
            global kon_y1_Ux
            global kon_y2_Ux
            global kon_y1_Uy
            global kon_y2_Uy
 

            self.treeview.setEnabled(False)
            self.item = QtGui.QListWidgetItem("Выполняется процесс решения...", self.listWidget)
            self.color = QtGui.QColor("blue")
            self.item.setTextColor(self.color)
            self.listWidget.addItem(self.item)

            file = open(full_dir+"/out_run.log", "w")
            proc = subprocess.Popen(["bash "+full_dir+"/SOLVER_BASH"], cwd = full_dir, shell = True, stdout=file, stderr=file)

            #...........................Отрисовка графиков................................

            t_mas = []
            ir_mas_Ux = []
            fr_mas_Ux = []
            ir_mas_Uy = []
            fr_mas_Uy = []
            file_r = open(full_dir+"/out_run.log", "r")
            while proc.poll() is None:
                for line in file_r.readlines():
                    time_reg = re.compile(r"Time\s=\s\S*\n")
                    time_mas = time_reg.findall(line)
                    x = np.array([])
                    if time_mas != []:
                    
                        time_div = time_mas[0].split(" ")
                        t_mas.append(time_div[2])

                        kon_x = np.append(x, t_mas)

                    res_reg_Ux = re.compile(r"\sUx,\sInitial\sresidual\s=\s\S*,\sFinal\sresidual\s=\s\S*")
                    res_mas_Ux = res_reg_Ux.findall(line)

                    res_reg_Uy = re.compile(r"\sUy,\sInitial\sresidual\s=\s\S*,\sFinal\sresidual\s=\s\S*")
                    res_mas_Uy = res_reg_Uy.findall(line)

                    y1_Ux = np.array([])
                    y2_Ux = np.array([])

                    y1_Uy = np.array([])
                    y2_Uy = np.array([])

                    if res_mas_Ux != []:
                        resid_reg_Ux = re.compile(r"(?<=[ ])\S*(?=[,])")
                        resid_mas_Ux = resid_reg_Ux.findall(res_mas_Ux[0])
                        ir_mas_Ux.append(resid_mas_Ux[1])
                        fr_mas_Ux.append(resid_mas_Ux[2])

                        kon_y1_Ux = np.append(y1_Ux, ir_mas_Ux)
                        kon_y2_Ux = np.append(y2_Ux, fr_mas_Ux)

                        #line, = plot(kon_x,kon_y1)
                        #line, = plot(kon_x,kon_y2)
                         
                        #pause(0.2)

                        #pylab.plot(kon_x, kon_y1_Ux)
                        #pylab.plot(kon_x, kon_y2_Ux)
                        #pylab.title("График сходимости Ux")

                        #pylab.show()

                        #pause(0.2)
                    if res_mas_Uy != []:
                        resid_reg_Uy = re.compile(r"(?<=[ ])\S*(?=[,])")
                        resid_mas_Uy = resid_reg_Uy.findall(res_mas_Uy[0])
                        ir_mas_Uy.append(resid_mas_Uy[1])
                        fr_mas_Uy.append(resid_mas_Uy[2])

                        kon_y1_Uy = np.append(y1_Uy, ir_mas_Uy)
                        kon_y2_Uy = np.append(y2_Uy, fr_mas_Uy)

                        #line, = plot(kon_x,kon_y1)
                        #line, = plot(kon_x,kon_y2)
                         
                        #pause(0.2)

                        #pylab.plot(kon_x, kon_y1_Ux)
                        #pylab.plot(kon_x, kon_y2_Ux)
                        #pylab.title("График сходимости Ux")

                        #pylab.show()

                        #pause(0.2)
                        pylab.subplot (2, 1, 1)
                        pylab.title("Residual Ux")
                        #pylab.plot(kon_x, kon_y1_Ux)
                        pylab.plot(kon_x, kon_y2_Ux)
                        pylab.xlabel("Time, s")
                        pylab.ylabel("Ux")
                        pylab.yscale('log')

                        #ts.plot(logy=True);
                        
                        pylab.subplot (2, 1, 2)
                        pylab.title("Residual Uy")
                        #pylab.plot(kon_x, kon_y1_Uy)
                        pylab.plot(kon_x, kon_y2_Uy)
                        pylab.xlabel("Time, s")
                        pylab.ylabel("Uy")
                        pylab.yscale('log')
                        

                        pause(0.2)

                time.sleep(0.5)

            if proc.returncode == 0:
                self.item = QtGui.QListWidgetItem("Процесс решения завершен", self.listWidget)
                self.color = QtGui.QColor("green")
                self.item.setTextColor(self.color)
                self.listWidget.addItem(self.item)
            
            else:
                self.item = QtGui.QListWidgetItem("Процесс решения остановлен", self.listWidget)
                self.color = QtGui.QColor("red")
                self.item.setTextColor(self.color)
                self.listWidget.addItem(self.item)

                self.treeview.setEnabled(True)

        # ...........................Функция запуска второго потока...........................

        def on_task_close():
            self.t2.start()

        # ...........................Функция запуска третьего потока...........................

        def on_view_open():
            f = open(full_dir+'/VIEW_BASH', 'w')
            f.write('#!/bin/sh' + '\n' + '. /opt/openfoam231/etc/bashrc' + '\n' + 'paraFoam' + '\n' + 'exit')
            f.close()

            self.t3.start()
        
# ---------------------------Панель управления программой-----------------------------

        self.mesh_open = QtGui.QAction(self)
        self.mesh_open.setEnabled(True)
        mesh_ico = self.style().standardIcon(
                             QtGui.QStyle.SP_DirOpenIcon)
        self.mesh_open.setIcon(mesh_ico)
        self.mesh_open.setToolTip('Открыть форму импорта сетки')

        self.task_open = QtGui.QAction(self)
        self.task_open.setEnabled(True)
        task_ico = self.style().standardIcon(
                             QtGui.QStyle.SP_FileDialogStart)
        self.task_open.setIcon(task_ico)
        self.task_open.setToolTip('Запустить процесс решения')

        self.task_close = QtGui.QAction(self)
        self.task_close.setEnabled(True)
        close_ico = self.style().standardIcon(
                             QtGui.QStyle.SP_DockWidgetCloseButton)
        self.task_close.setIcon(close_ico)
        self.task_close.setToolTip('Остановить процесс решения')

        self.view_open = QtGui.QAction(self)
        self.view_open.setEnabled(True)
        view_ico = self.style().standardIcon(
                             QtGui.QStyle.SP_DriveNetIcon)
        self.view_open.setIcon(view_ico)
        self.view_open.setToolTip('Запустить parafoam')

        self.toolBar = QtGui.QToolBar("MyToolBar")
        self.toolBar.addAction(self.mesh_open)
        self.toolBar.addAction(self.task_open)
        self.toolBar.addAction(self.task_close)
        self.toolBar.addAction(self.view_open)

        self.mesh_open.triggered.connect(on_mesh_open)
        self.task_open.triggered.connect(on_task_open)
        self.task_close.triggered.connect(on_task_close)
        self.view_open.triggered.connect(on_view_open)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

# -----------------------Верхний виджет с названием проекта---------------------------

        self.pnl = QtGui.QDockWidget()
        self.pnl.setFixedSize(1000, 50)
        self.pnl.setFeatures(self.pnl.NoDockWidgetFeatures)
        self.project_name_label = QtGui.QLabel("Название проекта: " + "<font color='peru'>"+prj_name+"</font>")
        self.project_name_label.setStyleSheet("border-style: none;")
        pnl_grid = QtGui.QGridLayout()
        pnl_grid.addWidget(self.project_name_label, 0, 0, alignment=QtCore.Qt.AlignLeft) 
        pnl_frame = QtGui.QFrame()
        pnl_frame.setStyleSheet("background-color: ghostwhite;" "border-width: 0.5px;" "border-style: solid;" "border-color: silver;")
        pnl_frame.setLayout(pnl_grid)
        self.pnl.setWidget(pnl_frame)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.pnl)

# -----------------Левый виджет с файловой системой проекта---------------------

        self.fsw = QtGui.QDockWidget()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.fsw)
        self.fsw.setFeatures(self.fsw.NoDockWidgetFeatures)
        self.fsw_label = QtGui.QLabel()
        self.fsw_label.setAlignment(QtCore.Qt.AlignCenter)
        self.fsw_grid = QtGui.QGridLayout()
        self.fsw_grid.addWidget(self.fsw_label, 0, 0)
        self.fsw_frame = QtGui.QFrame()
        self.fsw_frame.setFixedSize(406, 27)
        self.fsw_frame.setStyleSheet("background-color: honeydew;" "border-width: 1px;" "border-style: solid;" "border-color: dimgray;" "border-radius: 4px;")
        self.fsw_frame.setLayout(self.fsw_grid)
        fs_lbl = "Файловая структура проекта"
        self.fsw_label.setText("<font color='SeaGreen'>" + fs_lbl + "</font>")
        self.fsw_label.setStyleSheet("border-style: none;" "font-size: 8pt;")
        self.fsw.setTitleBarWidget(self.fsw_frame)
        self.treeview = QtGui.QTreeView()
        self.treeview.setMaximumWidth(400)
        self.treeview.setMinimumWidth(400)
        self.treeview.setFixedSize(400, 715)
        self.treeview.model = QtGui.QFileSystemModel() 
        self.treeview.model.setRootPath(full_dir) 
        self.treeview.setModel(self.treeview.model) 
        self.treeview.setColumnWidth(0, 100)  
        self.treeview.setColumnHidden(1, True)
        self.treeview.setColumnHidden(2, True)
        self.treeview.setColumnHidden(3, True)
        self.treeview.header().hide()
        self.treeview.setRootIndex(self.treeview.model.index(full_dir))    
        self.treeview.model.directoryLoaded.connect(self.fetchAndExpand)
        self.treeview.setItemsExpandable(False)       
        self.treeview.clicked.connect(self.on_treeview_clicked)
        self.fsw.setWidget(self.treeview)

# -----------------Центральный виджет с формой параметров---------------------

        self.ffw = QtGui.QDockWidget()
        self.ffw.setFeatures(self.ffw.NoDockWidgetFeatures)
        self.ffw_label = QtGui.QLabel()
        self.ffw_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ffw_grid = QtGui.QGridLayout()
        self.ffw_grid.addWidget(self.ffw_label, 0, 0)
        self.ffw_frame = QtGui.QFrame()
        self.ffw_frame.setFixedSize(590, 28)
        self.ffw_frame.setStyleSheet("border-width: 1px;" "border-style: solid;" "border-color: dimgray;" "border-radius: 4px;" "background-color: honeydew;")
        self.ffw_frame.setLayout(self.ffw_grid)
        
# ---------------------Нижний виджет со служебными сообщениями------------------------

        self.serv_mes = QtGui.QDockWidget("Служебные сообщения")
        self.serv_mes.setFixedSize(1000, 170)
        self.serv_mes.setFeatures(self.serv_mes.NoDockWidgetFeatures)
        self.listWidget = QtGui.QListWidget()
        self.serv_mes.setWidget(self.listWidget)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.serv_mes)

# -----------------------------Функции главной формы----------------------------------

# .......................Функция рскрытия дерева файлов проекта.......................

    def fetchAndExpand(self, full_dir):
        index = self.treeview.model.index(full_dir)
        self.treeview.expand(index)  
        for i in range(self.treeview.model.rowCount(index)):
            child = index.child(i, 0)
            if self.treeview.model.isDir(child) and self.treeview.model.fileName(child) == "0" or self.treeview.model.fileName(child) == "system" or self.treeview.model.fileName(child) == "constant" or self.treeview.model.fileName(child) == "polyMesh":
                self.treeview.model.setRootPath(self.treeview.model.filePath(child))

# ...........................Функция клика по файлу из дерева.........................

    def on_treeview_clicked(self, index):
        global fileName
        indexItem = self.treeview.model.index(index.row(), 0, index.parent())
        file_name = self.treeview.model.fileName(indexItem)
        file_form_class.inp_file_form_func(self, file_name)
        file_name_title = file_form_class.out_file_name_func()
        if file_name_title != None:
            self.setCentralWidget(self.ffw)
            
            self.ffw.setTitleBarWidget(self.ffw_frame)
            self.ffw_label.setText("Форма параметров файла: " + "<font color='peru'>" + file_name_title + "</font>")
            self.ffw_label.setStyleSheet("border-style: none;" "font-size: 8pt;")
        else:
            self.clear_label = QtGui.QLabel()
            self.ffw.setTitleBarWidget(self.clear_label)
            
        file_form = file_form_class.out_file_form_func()
        self.ffw.setWidget(file_form)

# ...........................Функция начала процесса визуализации..........................

    def on_t3_started(self):
        time.sleep(8)

        self.item = QtGui.QListWidgetItem("parafoam успешно запущен", self.listWidget)
        self.color = QtGui.QColor("green")
        self.item.setTextColor(self.color)
        self.listWidget.addItem(self.item)

# .......................Формирование главного окна программы.........................

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Настройка параметров")
    window.setFixedSize(1000, 1000)
    window.setGeometry(500, 100, 1000, 1000)
    window.show()
    sys.exit(app.exec_())
       
