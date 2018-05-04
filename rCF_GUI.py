# -*- coding: utf-8 -*-
# -------------------------------Импорт модулей----------------------------------
from PyQt4 import QtCore, QtGui
import shutil
import sys
import re
import os
import os.path
from forms.file_system import MainWindow

# ---------------------------Главная форма проекта-------------------------------

class Project_Form(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
# ------------------------Функции связанные с формой-----------------------------

# .....Функция, запускаемая при нажатии радио-кнопки "создать новый проект"......
        def on_np_clicked():
            if np_radio.isChecked():
                title_label.setEnabled(True)
                project_frame.setEnabled(True)
                project_frame.setStyleSheet("border-color: dimgray;")

# .....Функция, запускаемая при нажатии радио-кнопки "открыть имеющийся проект"......

        def on_cp_clicked():
            if cp_radio.isChecked():
                choice_button.setEnabled(True)
                title_label.setEnabled(False)
                project_frame.setEnabled(False)
                project_frame.setStyleSheet("border-color: darkgray;")
            else:
                choice_button.setEnabled(False)

# .....Функция, запускаемая при нажатии кнопки "выбрать имеющийся проект"......

        def on_chbtn_clicked():
            global directory
            folder_dir = QtGui.QFileDialog.getExistingDirectory(directory=QtCore.QDir.currentPath())
            directory, project_name_dir = os.path.split(folder_dir)
            #dir_reg = re.compile(r"\S*(?<=[\/])run(?![\/])")
            #dir_mas = dir_reg.findall(directory)
            #if dir_mas != []:
            path_button.setEnabled(False)
            title_label.setEnabled(True)
            project_frame.setEnabled(True)
            project_frame.setStyleSheet("border-color: dimgray;")
            project_name.setEnabled(False)
            project_name.setStyleSheet("border-color: silver;")
            project_path_name.setEnabled(False)
            project_path_name.setStyleSheet("border-color: silver;")
            app_name.setEnabled(False)

# --------------------------Функции связанные c выводом-----------------------------

            file = open(folder_dir+"/system/controlDict", 'r') 
            data = file.read()
            file.close()
            app_reg = re.compile(r"(?<=[ ])\S*(?=[;])")
            app_mas = app_reg.findall(data)
            mas = app_name.count()
            for i in range(mas):
                if app_name.itemText(i) == app_mas[5]:
                    app_name.setCurrentIndex(i)
        
            project_name.setText(project_name_dir)
            project_path_name.setText(directory)

            file = open(folder_dir+"/system/controlDict", 'r') 
            data = file.read()
            file.close()

            a_reg = re.compile(r"(?<=[ ])\S*(?=[;])")
            a_mas = a_reg.findall(data)
            app_name.setEditText(a_mas[5])
            index = app_name.findText(a_mas[5], QtCore.Qt.MatchFixedString)
            app_name.setCurrentIndex(index)

            if os.path.exists(folder_dir+"/system/decomposeParDict") == True:
                rsp_label.setEnabled(True)
                rsp_frame.setEnabled(True)
                rsp_frame.setStyleSheet("border-color: dimgray;")
                rsp_radio.setChecked(True)

                file = open(folder_dir+"/system/decomposeParDict", 'r') 
                data = file.read()
                file.close()

                nos_reg = re.compile(r"(?<=[ ])\S*(?=[;])")
                nos_mas = nos_reg.findall(data)
                nos_edit.setValue(int(nos_mas[5]))
                index = m_name.findText(nos_mas[6], QtCore.Qt.MatchFixedString)
                m_name.setCurrentIndex(index)

            #else:
                #dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                                           #"Внимание!", "Это не проект",
                                           #buttons = QtGui.QMessageBox.Ok)
                #result = dialog.exec_()

# .....Функция, запускаемая при нажатии кнопки выбора директории сохранения нового проекта"......

        def on_path_choose():
            global directory

            directory = QtGui.QFileDialog.getExistingDirectory(directory=QtCore.QDir.currentPath())
            dir_reg = re.compile(r"\S*(?<=[\/])run(?![\/])")
            dir_mas = dir_reg.findall(directory)

            project_path_name.setText(directory)

            #if dir_mas!=[]:
                #project_path_name.setText(directory)
            #else:
                #dialog = QtGui.QMessageBox(QtGui.QMessageBox.Critical,
                    #"Внимание!", "Это не директория 'run' проектов OpenFOAM", buttons = QtGui.QMessageBox.Ok)
                #result = dialog.exec_()
                
# .....Функция, запускаемая при завершении редактирования названия проекта и его директории"......

        def handleEditingFinished():
            if project_name.text() and project_path_name.text():
                save_button.setEnabled(True)
        
# ....................Функция, запускаемая при нажатии кнопки "сохранить"....................
        
        def on_save_clicked():

            if np_radio.isChecked():
                shutil.copytree("./matches/Шаблон проекта", directory+"/"+project_name.text())

            file = open(project_path_name.text()+"/"+project_name.text()+"/system/controlDict", 'r')
            data = file.read()
            file.close()

            a = app_name.currentText()
            a_reg = re.compile(r"application\s*\S*\;")
            data = re.sub(a_reg,"application"+"     "+a+";", data)

            file = open(project_path_name.text()+"/"+project_name.text()+"/system/controlDict", 'w')
            file.write(data)
            file.close()

            app_glob = app_name.currentText()
            self.close()
            
            project_name_dir = project_name.text()
            MW = MainWindow(directory, project_name_dir, app_glob)
            MW.setWindowTitle('Главное окно программы')
            MW.setFixedSize(1000, 1000)
            MW.setGeometry(500, 100, 1000, 1000)
            MW.show()

# .....................Функция, запускаемая при нажатии кнопки "отмена"......................
        
        def on_cancel_clicked():
            self.close()

# ------------------------------------Первый блок формы--------------------------------------

        choice_label = QtGui.QLabel("Создайте новый проект или откройте имеющийся")
        cl_hbox = QtGui.QHBoxLayout()
        cl_hbox.addWidget(choice_label)
        np_radio = QtGui.QRadioButton("Создать новый проект")
        np_radio.toggled.connect(on_np_clicked)
        cp_radio = QtGui.QRadioButton("Открыть имеющийся проект")
        cp_radio.toggled.connect(on_cp_clicked)
        icon = self.style().standardIcon(QtGui.QStyle.SP_DirOpenIcon)
        choice_button = QtGui.QPushButton()
        choice_button.setFixedSize(30, 30)
        choice_button.setIcon(icon)
        choice_button.setEnabled(False)
        choice_button.clicked.connect(on_chbtn_clicked)
        ch_grid = QtGui.QGridLayout()
        ch_grid.addWidget(np_radio, 0, 0)
        ch_grid.addWidget(cp_radio, 0, 1)
        ch_grid.addWidget(choice_button, 0, 2)
        ch_frame = QtGui.QFrame()
        ch_frame.setFrameShape(QtGui.QFrame.Panel)
        ch_frame.setFrameShadow(QtGui.QFrame.Sunken)
        ch_frame.setLayout(ch_grid)
        ch_hbox = QtGui.QHBoxLayout() 
        ch_hbox.addWidget(ch_frame)
        
# -------------------------------------Второй блок формы------------------------------------

        title_label = QtGui.QLabel("Введите название задачи и укажите директорию и решатель")
        title_label.setEnabled(False)
        tl_hbox = QtGui.QHBoxLayout()
        tl_hbox.addWidget(title_label)
        project_label = QtGui.QLabel("Название проекта:") 
        project_name = QtGui.QLineEdit()
        project_name.textChanged.connect(handleEditingFinished)
        project_name.setFixedSize(180, 25)
        valid = QtGui.QRegExpValidator(QtCore.QRegExp("\S*"), self)
        project_name.setValidator(valid)
        project_path_label = QtGui.QLabel("Путь:")
        project_path_name = QtGui.QLineEdit()
        project_path_name.setEnabled(False)
        project_path_name.textChanged.connect(handleEditingFinished)
        project_path_name.setFixedSize(180, 25)
        path_button = QtGui.QPushButton("...")
        path_button.clicked.connect(on_path_choose)
        path_button.setFixedSize(25, 25)
        app_label = QtGui.QLabel("Решатель:")
        app_name = QtGui.QComboBox()
        app_name.addItems("rhoCentralFoam".split())
        app_name.setFixedSize(180, 25)
        project_grid = QtGui.QGridLayout()
        project_grid.addWidget(project_label, 0, 0)
        project_grid.addWidget(project_name, 0, 1, alignment=QtCore.Qt.AlignRight)
        project_grid.addWidget(project_path_label, 1, 0)
        project_grid.addWidget(project_path_name, 1, 1)
        project_grid.addWidget(app_label, 2, 0)
        project_grid.addWidget(app_name, 2, 1)
        project_grid.addWidget(path_button, 1, 2)
        project_frame = QtGui.QFrame()
        project_frame.setEnabled(False)
        project_frame.setStyleSheet("border-color: darkgray;")
        project_frame.setFrameShape(QtGui.QFrame.Panel)
        project_frame.setFrameShadow(QtGui.QFrame.Sunken)
        project_frame.setLayout(project_grid) 
        project_grid_vbox = QtGui.QVBoxLayout() 
        project_grid_vbox.addWidget(project_frame)

# ---------------------Кнопки сохранения и отмены и их блок-------------------------

        save_button = QtGui.QPushButton("Сохранить")
        save_button.clicked.connect(on_save_clicked)
        save_button.setEnabled(False)
        cancel_button = QtGui.QPushButton("Отмена")
        cancel_button.clicked.connect(on_cancel_clicked)
        buttons_hbox = QtGui.QHBoxLayout()
        buttons_hbox.addWidget(save_button)
        buttons_hbox.addWidget(cancel_button)

# -----------------------Размещение компонентов на форме----------------------------

        form_1 = QtGui.QFormLayout()
        form_1.addRow(cl_hbox)
        form_1.addRow(ch_hbox)
        form_1.addRow(tl_hbox)
        form_1.addRow(project_grid_vbox)
        form_1.addRow(buttons_hbox)
        self.setLayout(form_1)

# -----------------------------Вывод формы на экране--------------------------------

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(open("./styles/main_form_style.qss","r").read())
    pf = Project_Form()
    pf.setGeometry(800, 300, 390, 200)
    pf.setWindowTitle("Форма параметров проекта")
    pf.show()
    sys.exit(app.exec_())
