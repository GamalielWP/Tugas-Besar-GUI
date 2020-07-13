import sys
import pyodbc
from login import *
from formadmin import *
from formpendaftar import *
from formdokter import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

con = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-4E2QUI3\SQLEXPRESS;'
                          'Database=db_puskesmas;'
                          'Trusted_Connection=yes;')
cur = con.cursor()
con.timeout = 0
con.autocommit = True
                          
def messagebox(title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

def create_log(nik, nama, ket):
    querry = 'EXEC sp_AddLogAdmin ?, ?, ?'
    cur.execute(querry, (nik, nama, ket))
    print(nik, nama, ket)
    
def logout():
    ket = 'Melakukan Logout'
    querry = 'SELECT * FROM view_autentikasi WHERE nik = ?'
    cur.execute(querry, (loginMain.nik))
    records = cur.fetchall()
    create_log(records[0][0], records[0][3], ket)
    
class loginMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login = Ui_loginForm()
        self.login.setupUi(self)
        self.show()
        
        self.login.linePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.loginButton.clicked.connect(self.autentikasi)
    
    def autentikasi(self):
        # try:
        global sps
        global tbl
        ket = "Melakukan Login"
        nik = self.login.lineNIK.text()
        psw = self.login.linePassword.text()
        querry = 'SELECT * FROM view_autentikasi WHERE nik = ? AND _password = ?'
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
                querry = 'SELECT * FROM view_daftar_dokter_spesialis WHERE NIK = ?'
                cur.execute(querry, (nik))
                records = cur.fetchall()
                loginMain.sps = records[0][2]
                loginMain.tbl = records[0][3]
                self.form = formdokter()
                self.form.show()
                self.close()
            else:
                print('Something went wrong')
        else:
            messagebox("Autentikasi", "Login Gagal")
        # except:
            # messagebox("Autentikasi", "Login Gagal")
    
class formadmin(QWidget):
    def __init__(self):
        super().__init__()
        self.formadmin = Ui_FormAdmin()
        self.formadmin.setupUi(self)
        
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        
        self.formadmin.tableLogLogin.setColumnCount(4)
        self.formadmin.tableLogLogin.setHorizontalHeaderLabels(('NIK', 'Nama', 'Waktu', 'Keterangan'))
        self.formadmin.tableLogLogin.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.formadmin.tableLogLogin.verticalHeader().setVisible(False)
        
        self.formadmin.tablePegawai.setColumnCount(4)
        self.formadmin.tablePegawai.setHorizontalHeaderLabels(('NIK', 'Nama', 'Jabatan', 'Alamat'))
        self.formadmin.tablePegawai.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.formadmin.tablePegawai.verticalHeader().setVisible(False)
        
        self.formadmin.hapusButton.setEnabled(False)
        self.formadmin.editButton.setEnabled(False)
        
        self.formadmin.label_nama_adm.setText(loginMain.nama)
        self.formadmin.label_nik_adm.setText(loginMain.nik)
        
        self.timer.timeout.connect(self.bacadaftarpgw)
        self.timer.timeout.connect(self.bacalogpgw)
        
        self.formadmin.button_logout.clicked.connect(self.logoutini)
        self.formadmin.pushButton_3.clicked.connect(self.createpgw)
        self.formadmin.tablePegawai.itemClicked.connect(self.selectpgw)
        self.formadmin.editButton.clicked.connect(self.updatepgw)
        self.formadmin.hapusButton.clicked.connect(self.deletepgw)
        self.formadmin.pushButton_6.clicked.connect(self.clearall)
        self.formadmin.cariButton.clicked.connect(self.search)
        self.formadmin.refreshButton.clicked.connect(self.refresh)
    
    def refresh(self):
        self.timer.start(1000)
        self.formadmin.linePencarian.clear()
    
    def bacadaftarpgw(self):
        querry = 'SELECT * FROM view_daftar_pegawai'
        cur.execute(querry)
        self.formadmin.tablePegawai.setRowCount(0)
        
        for row_number, row_data in enumerate(cur):
            self.formadmin.tablePegawai.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.formadmin.tablePegawai.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                
    def bacalogpgw(self):
        querry = 'SELECT * FROM log_login_karyawan'
        cur.execute(querry)
        self.formadmin.tableLogLogin.setRowCount(0)
        
        for row_number, row_data in enumerate(cur):
            self.formadmin.tableLogLogin.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.formadmin.tableLogLogin.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
                
    def search(self):
        self.timer.stop()
        cari = self.formadmin.linePencarian.text()
        print('mencari ' + cari)
        querry = 'SELECT * FROM fx_CariPegawai(?)'
        cur.execute(querry, (cari))
        self.formadmin.tablePegawai.setRowCount(0)
        
        for row_number, row_data in enumerate(cur):
            self.formadmin.tablePegawai.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.formadmin.tablePegawai.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        
    def createpgw(self):
        try:
            nik = self.formadmin.lineNIK.text()
            nama1 = self.formadmin.lineNama.text()
            nama2 = self.formadmin.lineNama_2.text()
            pw = self.formadmin.line_password.text()
            alamat = self.formadmin.lineAlamat.text()
            kontak = self.formadmin.lineKontak.text()
            if self.formadmin.comboBox.currentIndex() == 1:
                jbt = 'adm'
            elif self.formadmin.comboBox.currentIndex() == 2:
                jbt = 'doc'
            elif self.formadmin.comboBox.currentIndex() == 3:
                jbt = 'kwn'
            querry = 'INSERT INTO data_karyawan(NIK, _password, jabatan, nama_a, nama_b, alamat, kontak) VALUES (?, ?, ?, ?, ?, ?, ?)'
            cur.execute(querry, (nik, pw, jbt, nama1, nama2, alamat, kontak))
            messagebox('Sukses', 'Data Pegawai Baru Berhasil Dibuat')
            self.clearall()
            ket = ('menambahkan pegawai baru ' + nik)
            create_log(self.formadmin.label_nik_adm.text(), self.formadmin.label_nama_adm.text(), ket)
        except:
            messagebox('Gagal', 'Data Pegawai Baru Tidak Berhasil Dibuat')
        
    def selectpgw(self):
        self.formadmin.groupBox_2.setTitle('Update Data')
        indexes = []
        for selectionRange in self.formadmin.tablePegawai.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
        for i in indexes:
            nik = self.formadmin.tablePegawai.item(i, 0).text()
        querry = 'SELECT * FROM data_karyawan WHERE NIK = ?'
        cur.execute(querry, (nik))
        records = cur.fetchall()
        self.formadmin.lineNIK.setText(records[0][0])
        self.formadmin.lineNIK.setEnabled(False)
        self.formadmin.lineNama.setText(records[0][3])
        self.formadmin.lineNama_2.setText(records[0][4])
        self.formadmin.line_password.setText(records[0][1])
        self.formadmin.lineAlamat.setText(records[0][5])
        self.formadmin.lineKontak.setText(records[0][6])
        if records[0][2] == 'adm':
            self.formadmin.comboBox.setCurrentIndex(1)
        elif records[0][2] == 'doc':
            self.formadmin.comboBox.setCurrentIndex(2)
        elif records[0][2] == 'kwn':
            self.formadmin.comboBox.setCurrentIndex(3)
        self.formadmin.comboBox.setEnabled(False)
        self.formadmin.pushButton_3.setEnabled(False)
        self.formadmin.hapusButton.setEnabled(True)
        self.formadmin.editButton.setEnabled(True)
        
    def updatepgw(self):
        try:
            nik = self.formadmin.lineNIK.text()
            nama1 = self.formadmin.lineNama.text()
            nama2 = self.formadmin.lineNama_2.text()
            pw = self.formadmin.line_password.text()
            alamat = self.formadmin.lineAlamat.text()
            kontak = self.formadmin.lineKontak.text()
            querry = 'UPDATE data_karyawan SET _password = ?, nama_a = ?, nama_b = ?, alamat = ?, kontak = ? WHERE NIK = ?'
            upd = cur.execute(querry, (pw, nama1, nama2, alamat, kontak, nik))
            if nik == self.formadmin.label_nik_adm.text():
                querry = 'SELECT * FROM view_autentikasi WHERE NIK = ?'
                data = cur.execute(querry, (nik))
                records = cur.fetchall()
                self.formadmin.label_nama_adm.setText(records[0][3])
            messagebox('BERHASIL', ('Berhasil mengupdate pegawai ' + nik))
            ket = ('mengupdate pegawai ' + nik)
            create_log(self.formadmin.label_nik_adm.text(), self.formadmin.label_nama_adm.text(), ket)
        except:
            messagebox('GAGAL', 'Gagal mengupdate')
        
    def deletepgw(self):
        try:
            nik = self.formadmin.lineNIK.text()
            if nik != self.formadmin.label_nik_adm.text():
                querry = 'DELETE FROM data_karyawan WHERE NIK = ?'
                dlt = cur.execute(querry, (nik))
                messagebox('BERHASIL', ('Berhasil Menghapus Pegawai ' + nik))
                self.clearall()
                ket = ('menghapus pegawai ' + nik)
                create_log(self.formadmin.label_nik_adm.text(), self.formadmin.label_nama_adm.text(), ket)
            else:
                messagebox('ERROR', 'Tidak Dapat Menghapus Diri Anda Sendiri')
        except:
            messagebox('GAGAL', 'Tidak Dapat Menghapus')
    
    def clearall(self):
        self.formadmin.groupBox_2.setTitle('Data Baru')
        self.formadmin.lineNIK.clear()
        self.formadmin.lineNIK.setEnabled(True)
        self.formadmin.lineNama.clear()
        self.formadmin.lineNama_2.clear()
        self.formadmin.line_password.clear()
        self.formadmin.lineAlamat.clear()
        self.formadmin.lineKontak.setText('+62')
        self.formadmin.comboBox.setEnabled(True)
        self.formadmin.pushButton_3.setEnabled(True)
        self.formadmin.editButton.setEnabled(False)
        self.formadmin.hapusButton.setEnabled(False)
    
    def logoutini(self):
        logout()
        self.form = loginMain()
        self.form.show()
        self.close()

class formdokter(QWidget):
    def __init__(self):
        super().__init__()
        self.formdokter = Ui_FormDokter()
        self.formdokter.setupUi(self)
        
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        
        global tbl
        global sps
        
        tbl = loginMain.tbl
        sps = loginMain.sps
        
        self.formdokter.tablePasien.setColumnCount(4)
        self.formdokter.tablePasien.setHorizontalHeaderLabels(('ID', 'Nama', 'Gender', 'Golongan Darah'))
        self.formdokter.tablePasien.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.formdokter.tablePasien.verticalHeader().setVisible(False)
        
        self.formdokter.label_nama_adm.setText(loginMain.nama)
        self.formdokter.label_nik_adm.setText(loginMain.nik)
        self.formdokter.label_14.setText(sps)
        
        self.formdokter.pushButton_3.setEnabled(False)
        self.formdokter.hapusButton.setEnabled(False)
        self.formdokter.lineRiwayat.setEnabled(False)
        
        self.timer.timeout.connect(self.bacadaftarpsn)
        
        self.formdokter.tablePasien.itemClicked.connect(self.selectpsn)
        self.formdokter.cariButton.clicked.connect(self.search)
        self.formdokter.pushButton_3.clicked.connect(self.updatepsn)
        self.formdokter.pushButton_6.clicked.connect(self.clearall)
        self.formdokter.hapusButton.clicked.connect(self.deletepsn)
        self.formdokter.refreshButton.clicked.connect(self.refresh)
        self.formdokter.button_logout.clicked.connect(self.logoutini)
    
    def refresh(self):
        self.timer.start(1000)
        self.formdokter.linePencarian.clear()
    
    def bacadaftarpsn(self):
        querry = 'SELECT * FROM ' + tbl + ' ORDER BY PasienId ASC'
        cur.execute(querry)
        self.formdokter.tablePasien.setRowCount(0)
        
        for row_number, row_data in enumerate(cur):
            self.formdokter.tablePasien.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.formdokter.tablePasien.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    
    def search(self):
        self.timer.stop()
        cari = self.formdokter.linePencarian.text()
        print('mencari ' + cari)
        querry = 'SELECT * FROM fx_CariPasienDokter(?, ?)'
        cur.execute(querry, (cari, sps))
        self.formdokter.tablePasien.setRowCount(0)
        
        for row_number, row_data in enumerate(cur):
            self.formdokter.tablePasien.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.formdokter.tablePasien.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    
    def selectpsn(self):
        global pid
        global nama
        indexes = []
        for selectionRange in self.formdokter.tablePasien.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
        for i in indexes:
            pid = self.formdokter.tablePasien.item(i, 0).text()
        querry = 'SELECT * FROM ' + tbl + ' WHERE PasienId = ?'
        cur.execute(querry, (pid))
        records = cur.fetchall()
        nama = records[0][1]
        self.formdokter.lineId.setText(str(records[0][0]))
        self.formdokter.lineNama.setText(records[0][1])
        self.formdokter.lineGender.setText(records[0][2])
        self.formdokter.lineGoldar.setText(records[0][3])
        self.formdokter.lineRiwayat.setPlainText(records[0][4])
        self.formdokter.pushButton_3.setEnabled(True)
        self.formdokter.hapusButton.setEnabled(True)
        self.formdokter.lineRiwayat.setEnabled(True)
    
    def updatepsn(self):
        try:
            riwayat = self.formdokter.lineRiwayat.toPlainText() 
            print(riwayat)
            querry = 'UPDATE ' + tbl + ' SET riwayat = ? WHERE PasienId = ?'
            cur.execute(querry, (riwayat, pid))
            messagebox('BERHASIL', ('Berhasil mengupdate data pasien ' + nama))
            ket = ('mengupdate pasien ' + nama)
            # create_log(self.formadmin.label_nik_adm.text(), self.formadmin.label_nama_adm.text(), ket)
        except:
            messagebox('GAGAL', 'Gagal mengupdate')
    
    def deletepsn(self):
        try:
            querry = 'DELETE FROM ' + tbl + ' WHERE PasienId = ?'
            dlt = cur.execute(querry, (pid))
            messagebox('BERHASIL', ('Berhasil Menghapus Pasien ' + nama))
            ket = ('menghapus pasien ' + nama)
            self.clearall()
            # create_log(self.formadmin.label_nik_adm.text(), self.formadmin.label_nama_adm.text(), ket)
        except:
            messagebox('GAGAL', 'Tidak Dapat Menghapus')
    
    def clearall(self):
        self.formdokter.lineId.clear()
        self.formdokter.lineNama.clear()
        self.formdokter.lineGender.clear()
        self.formdokter.lineGoldar.clear()
        self.formdokter.lineRiwayat.clear()
        self.formdokter.pushButton_3.setEnabled(False)
        self.formdokter.hapusButton.setEnabled(False)
        self.formdokter.lineRiwayat.setEnabled(False)
    
    def logoutini(self):
        logout()
        self.form = loginMain()
        self.form.show()
        self.close()
    
class formpendaftar(QWidget):
    def __init__(self):
        super().__init__()
        self.formpendaftar = Ui_FormPendaftar()
        self.formpendaftar.setupUi(self)
        
        self.timer = QtCore.QTimer()
        self.timer.start(1000)
        
        self.formpendaftar.tablePasien.setColumnCount(4)
        self.formpendaftar.tablePasien.setHorizontalHeaderLabels(('No', 'Nama', 'Jenis Kelamin', 'Keperluan'))
        self.formpendaftar.tablePasien.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.formpendaftar.tablePasien.verticalHeader().setVisible(False)
        
        self.formpendaftar.dateLahir.setDate(QDate.currentDate())
        self.formpendaftar.radioHeli.setChecked(True)
        
        self.formpendaftar.hapusButton.setEnabled(False)
        self.formpendaftar.editButton.setEnabled(False)
        
        self.formpendaftar.label_nama_adm.setText(loginMain.nama)
        self.formpendaftar.label_nik_adm.setText(loginMain.nik)
        
        self.timer.timeout.connect(self.bacadaftarpsn)
        
        self.formpendaftar.pushButton_3.clicked.connect(self.createpsn)
        self.formpendaftar.cariButton.clicked.connect(self.search)
        self.formpendaftar.refreshButton.clicked.connect(self.refresh)
        self.formpendaftar.tablePasien.itemClicked.connect(self.selectpsn)
        self.formpendaftar.editButton.clicked.connect(self.updatepsn)
        self.formpendaftar.hapusButton.clicked.connect(self.deletepsn)
        self.formpendaftar.pushButton_6.clicked.connect(self.clearall)
        self.formpendaftar.button_logout.clicked.connect(self.logoutini)
        
    def refresh(self):
        self.timer.start(1000)
        self.formpendaftar.linePencarian.clear()
    
    def bacadaftarpsn(self):
        querry = 'SELECT * FROM view_daftar_pasien ORDER BY PasienId ASC'
        cur.execute(querry)
        self.formpendaftar.tablePasien.setRowCount(0)
        
        for row_number, row_data in enumerate(cur):
            self.formpendaftar.tablePasien.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.formpendaftar.tablePasien.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    
    def search(self):
        self.timer.stop()
        cari = self.formpendaftar.linePencarian.text()
        print('mencari ' + cari)
        querry = 'SELECT * FROM fx_CariPasien(?)'
        cur.execute(querry, (cari))
        self.formpendaftar.tablePasien.setRowCount(0)
        
        for row_number, row_data in enumerate(cur):
            self.formpendaftar.tablePasien.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.formpendaftar.tablePasien.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    
    def createpsn(self):
        try:
            nama1 = self.formpendaftar.lineNama.text()
            nama2 = self.formpendaftar.lineNama_2.text()
            tempatl = self.formpendaftar.lineTempatLahir.text()
            tanggall = self.formpendaftar.dateLahir.date().toString('yyyy-MM-dd')
            if self.formpendaftar.radioLaki.isChecked():
                gender = 'Laki-laki'
            elif self.formpendaftar.radioLadies.isChecked():
                gender = 'Perempuan'
            elif self.formpendaftar.radioHeli.isChecked():
                gender = 'Apache Attack Helicopter'
            goldar = self.formpendaftar.comboGoldar.currentText()
            alamat = self.formpendaftar.lineAlamat.text()
            kontak = self.formpendaftar.lineEdit_7.text()
            keperluan = self.formpendaftar.comboBox.currentText()
            kpl = self.formpendaftar.comboBox.currentIndex()
            querry = 'EXEC sp_AddPatient ?, ?, ?, ?, ?, ?, ?, ?, ?'
            cur.execute(querry, (nama1, nama2, tempatl, tanggall, gender, goldar, alamat, kontak, kpl))
            messagebox('Sukses', 'Data Pasien Baru Berhasil Dibuat')
            self.clearall()
            ket = ('menambahkan pasien baru ' + nama1 + ' ' + nama2)
            # create_log(self.formpendaftar.label_nik_adm.text(), self.formpendaftar.label_nama_adm.text(), ket)
        except:
            messagebox('Gagal', 'Data Pasien Baru Tidak Berhasil Dibuat')
    
    def selectpsn(self):
        global pid
        self.formpendaftar.groupBox_2.setTitle('Update Data')
        indexes = []
        for selectionRange in self.formpendaftar.tablePasien.selectedRanges():
            indexes.extend(range(selectionRange.topRow(), selectionRange.bottomRow()+1))
        for i in indexes:
            pid = self.formpendaftar.tablePasien.item(i, 0).text()
        querry = 'SELECT * FROM data_pasien WHERE PasienId = ?'
        cur.execute(querry, (pid))
        records = cur.fetchall()
        self.formpendaftar.lineNama.setText(records[0][1])
        self.formpendaftar.lineNama_2.setText(records[0][2])
        self.formpendaftar.lineTempatLahir.setText(records[0][3])
        strdate = records[0][4]
        date = strdate.split('-')
        for i in range(0, len(date)): 
            date[i] = int(date[i]) 
        self.formpendaftar.dateLahir.setDate(QDate(date[0], date[1], date[2]))
        if records[0][5] == 'Laki-laki':
            self.formpendaftar.radioLaki.setChecked(True)
        elif records[0][5] == 'Perempuan':
            self.formpendaftar.radioLadies.setChecked(True)
        elif records[0][5] == 'Apache Attack Helicopter':
            self.formpendaftar.radioHeli.setChecked(True)
        self.formpendaftar.comboGoldar.setCurrentText(records[0][6])
        self.formpendaftar.lineAlamat.setText(records[0][7])
        self.formpendaftar.lineEdit_7.setText(records[0][8])
        self.formpendaftar.pushButton_3.setEnabled(False)
        self.formpendaftar.hapusButton.setEnabled(True)
        self.formpendaftar.editButton.setEnabled(True)
    
    def updatepsn(self):
        try:
            nama1 = self.formpendaftar.lineNama.text()
            nama2 = self.formpendaftar.lineNama_2.text()
            tempatl = self.formpendaftar.lineTempatLahir.text()
            tanggall = self.formpendaftar.dateLahir.date().toString('yyyy-MM-dd')
            if self.formpendaftar.radioLaki.isChecked():
                gender = 'Laki-laki'
            elif self.formpendaftar.radioLadies.isChecked():
                gender = 'Perempuan'
            elif self.formpendaftar.radioHeli.isChecked():
                gender = 'Apache Attack Helicopter'
            goldar = self.formpendaftar.comboGoldar.currentText()
            alamat = self.formpendaftar.lineAlamat.text()
            kontak = self.formpendaftar.lineEdit_7.text()
            keperluan = self.formpendaftar.comboBox.currentText()
            kpl = self.formpendaftar.comboBox.currentIndex()
            querry = 'UPDATE data_pasien SET nama_a = ?, nama_b = ?, tempat_lahir = ?, tanggal_lahir = ?, gender = ?, goldar = ?, alamat = ?, kontak = ?, Keperluan = ? WHERE PasienId = ?'
            cur.execute(querry, (nama1, nama2, tempatl, tanggall, gender, goldar, alamat, kontak, kpl, pid))
            messagebox('BERHASIL', ('Berhasil mengupdate data pasien ' + nama1 + ' ' + nama2))
            ket = ('mengupdate pasien ' + nama1 + ' ' + nama2)
            # create_log(self.formadmin.label_nik_adm.text(), self.formadmin.label_nama_adm.text(), ket)
        except:
            messagebox('GAGAL', 'Gagal mengupdate')
    
    def deletepsn(self):
        try:
            nama1 = self.formpendaftar.lineNama.text()
            nama2 = self.formpendaftar.lineNama_2.text()
            querry = 'DELETE FROM data_pasien WHERE PasienId = ?'
            dlt = cur.execute(querry, (pid))
            messagebox('BERHASIL', ('Berhasil Menghapus Pasien ' + nama1 + ' ' + nama2))
            self.clearall()
            ket = ('menghapus pasien ' + nama1 + ' ' + nama2)
            # create_log(self.formadmin.label_nik_adm.text(), self.formadmin.label_nama_adm.text(), ket)
        except:
            messagebox('GAGAL', 'Tidak Dapat Menghapus')
    
    def clearall(self):
        self.formpendaftar.groupBox_2.setTitle('Data Baru')
        self.formpendaftar.lineNama.clear()
        self.formpendaftar.lineNama_2.clear()
        self.formpendaftar.lineTempatLahir.clear()
        self.formpendaftar.dateLahir.setDate(QDate.currentDate())
        self.formpendaftar.radioLaki.setChecked(False)
        self.formpendaftar.radioLadies.setChecked(False)
        self.formpendaftar.radioHeli.setChecked(True)
        self.formpendaftar.comboGoldar.setCurrentIndex(0)
        self.formpendaftar.lineAlamat.clear()
        self.formpendaftar.lineEdit_7.setText('+62')
        self.formpendaftar.comboBox.setCurrentIndex(0)
        self.formpendaftar.pushButton_3.setEnabled(True)
        self.formpendaftar.editButton.setEnabled(False)
        self.formpendaftar.hapusButton.setEnabled(False)
    
    def logoutini(self):
        logout()
        self.form = loginMain()
        self.form.show()
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = loginMain()
    sys.exit(app.exec_())