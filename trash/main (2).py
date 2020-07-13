import sys
import pyodbc
from login import *
from formadmin import *
from formpendaftar import *
from formdokter import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QTableView, QApplication
from PyQt5.QtWidgets import *

SERVER_NAME = 'DESKTOP-4E2QUI3\SQLEXPRESS'
DATABASE_NAME = 'db_puskesmas'
USERNAME = ''
PASSWORD = ''

def messagebox(title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

def createConnection():
    connString = f'DRIVER={{SQL Server}};'\
                f'SERVER={SERVER_NAME};'\
                f'DATABASE={DATABASE_NAME}'

    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(connString)
        
def displayData(sqlStatement):
    print('processing query...')
    qry = QSqlQuery(db)
    qry.prepare(sqlStatement)
    qry.exec()

    model = QSqlQueryModel()
    model.setQuery(qry)

    view = QTableView()
    view.setModel(model)
    return view    
    
def create_log(nik, nama, ket):
    con = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-4E2QUI3\SQLEXPRESS;'
                          'Database=db_puskesmas;'
                          'Trusted_Connection=yes;')
    con.timeout = 0
    con.autocommit = True
    cur = con.cursor()
    querry = 'EXEC sp_AddLogLogin ?, ?, ?'
    cur.execute(querry, (nik, nama, ket))
    print(nik, nama, ket)
    
class loginMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login = Ui_loginForm()
        self.login.setupUi(self)
        self.show()
        
        self.login.linePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.loginButton.clicked.connect(self.autentikasi)
    
    def autentikasi(self):
        try:
            ket = "Melakukan Login"
            nik = self.login.lineNIK.text()
            psw = self.login.linePassword.text()
            con = pyodbc.connect('Driver={SQL Server};'
                                  'Server=DESKTOP-4E2QUI3\SQLEXPRESS;'
                                  'Database=db_puskesmas;'
                                  'Trusted_Connection=yes;')
            cur = con.cursor()
            querry = 'SELECT * FROM data_karyawan WHERE nik = ? AND _password = ?'
            cur.execute(querry, (nik, psw))
            records = cur.fetchall()
            loginMain.nama = records[0][3]
            loginMain.nik = records[0][0]
            if len(records)>0:
                messagebox("Autentikasi", "Login Berhasil")
                create_log(records[0][0], records[0][3], ket)
                if records[0][2] == 'adm':
                    self.form = formadmin()
                    self.form.show()
                    self.close()
                elif records[0][2] == 'kwn':
                    self.form = formpendaftar()
                    self.form.show()
                    self.close()
                elif records[0][2] == 'doc':
                    self.form = formdokter()
                    self.form.show()
                    self.close()
                else:
                    print('Something went wrong')
            else:
                messagebox("Autentikasi", "Login Gagal")
        except:
            messagebox("Autentikasi", "Login Gagal")
    
class formadmin(QWidget):
    def __init__(self):
        super().__init__()
        self.formadmin = Ui_FormAdmin()
        self.formadmin.setupUi(self)
        
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        
        self.formadmin.label_nama_adm.setText(loginMain.nama)
        self.formadmin.label_nik_adm.setText(loginMain.nik)
        
        self.formadmin.button_logout.clicked.connect(self.logout)
        self.timer.timeout.connect(self.loglogin)
                
    def loglogin(self):
        SQL_STATEMENT = 'SELECT * FROM log_login_karyawan'
        self.formadmin.tableLogLogin = displayData(SQL_STATEMENT)
        self.formadmin.tableLogLogin.show()
    
    def logout(self):
        ket = 'Melakukan Logout'
        con = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-4E2QUI3\SQLEXPRESS;'
                          'Database=db_puskesmas;'
                          'Trusted_Connection=yes;')
        cur = con.cursor()
        querry = 'SELECT * FROM data_karyawan WHERE nik = ?'
        cur.execute(querry, (loginMain.nik))
        records = cur.fetchall()
        create_log(records[0][0], records[0][3], ket)
        self.form = loginMain()
        self.form.show()
        self.close()

class formdokter(QWidget):
    def __init__(self):
        super().__init__()
        self.formdokter = Ui_FormDokter()
        self.formdokter.setupUi(self)
        
        self.formdokter.label_nama_adm.setText(loginMain.nama)
        self.formdokter.label_nik_adm.setText(loginMain.nik)
        
        self.formdokter.button_logout.clicked.connect(self.logout)
        
    def logout(self):
        ket = 'Melakukan Logout'
        con = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-4E2QUI3\SQLEXPRESS;'
                          'Database=db_puskesmas;'
                          'Trusted_Connection=yes;')
        cur = con.cursor()
        querry = 'SELECT * FROM data_karyawan WHERE nik = ?'
        cur.execute(querry, (loginMain.nik))
        records = cur.fetchall()
        create_log(records[0][0], records[0][3], ket)
        self.form = loginMain()
        self.form.show()
        self.close()
    
class formpendaftar(QWidget):
    def __init__(self):
        super().__init__()
        self.formpendaftar = Ui_FormPendaftar()
        self.formpendaftar.setupUi(self)
        
        self.formpendaftar.label_nama_adm.setText(loginMain.nama)
        self.formpendaftar.label_nik_adm.setText(loginMain.nik)
        
        # self.formpendaftar.cariButton.clicked.connect(self.mencari)
        # self.formpendaftar.refreshButton.clicked.connect(self.refresh)
        # self.formpendaftar.editButtom.clicked.connect(self.edit)
        # self.formpendaftar.hapusButton.clicked.connect(self.hapus)
        
        self.formpendaftar.button_logout.clicked.connect(self.logout)
        
    def logout(self):
        ket = 'Melakukan Logout'
        con = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-4E2QUI3\SQLEXPRESS;'
                          'Database=db_puskesmas;'
                          'Trusted_Connection=yes;')
        cur = con.cursor()
        querry = 'SELECT * FROM data_karyawan WHERE nik = ?'
        cur.execute(querry, (loginMain.nik))
        records = cur.fetchall()
        create_log(records[0][0], records[0][3], ket)
        self.form = loginMain()
        self.form.show()
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = loginMain()
    sys.exit(app.exec_())