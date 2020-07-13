/*membuat dan menggunakan database puskesmas*/
CREATE DATABASE db_puskesmas

USE db_puskesmas

/*membuat table data_karyawan beserta input data samplenya*/
CREATE TABLE data_karyawan (NIK VARCHAR(8) PRIMARY KEY,
_password VARCHAR(20) NOT NULL, jabatan VARCHAR(3), nama_a VARCHAR(30), nama_b VARCHAR(30), alamat VARCHAR(50), kontak VARCHAR(14))

INSERT INTO data_karyawan (NIK, _password, jabatan, nama_a, nama_b , alamat, kontak)
	VALUES	('18104002', '18104002', 'adm', 'Agus', 'Safrudin', 'Jalan Wangon', '+6281234567890'),
			('18104010', '18104010', 'kwn', 'Gamal', 'Wigi', 'Jalan Blitar', '+6280112112123'),
			('18104003', '18104003', 'doc', 'Aji', 'Setyawan', 'Jalan Purwokerto', '+6282345398732'),
			('18104018', '18104018', 'doc', 'Yora', 'Putri', 'Jalan Indramayu', '+6289145439237'),
			('18104049', '18104049', 'doc', 'Zaky', 'Fatayan', 'Jalan Bumiayu', '+628880121884')

/*membuat table data_pasien*/
CREATE TABLE data_pasien (PasienId INT NOT NULL IDENTITY(00001,1), nama_a VARCHAR(30), nama_b VARCHAR(30),
tempat_lahir VARCHAR(50), tanggal_lahir DATE, gender VARCHAR(24) NOT NULL CHECK (gender IN('Laki-laki', 'Perempuan', 'Apache Attack Helicopter')),
goldar VARCHAR(2) NOT NULL CHECK (goldar IN('A', 'B', 'AB', 'O')), alamat VARCHAR(50), kontak VARCHAR(14), Keperluan VARCHAR(1) NOT NULL CHECK (keperluan IN('1', '2', '3')))

/*membuat table record kejadian pasien*/
CREATE TABLE log_data_pasien (NIK VARCHAR(8) NOT NULL, nama VARCHAR(30),
waktu DATETIME NOT NULL DEFAULT GETDATE(), keterangan VARCHAR(40))

/*membuat table jabatan_karyawan beserta input data samplenya*/
CREATE TABLE jabatan_karyawan (kode VARCHAR(3), jabatan VARCHAR(10))

INSERT INTO jabatan_karyawan(kode, jabatan)
	VALUES	('adm', 'Admin'),
			('kwn', 'Karyawan'),
			('doc', 'Dokter')

/*membuat table jabatan_karyawan beserta input data samplenya*/
CREATE TABLE kode_spesialisasi (kode VARCHAR(1), spesialisasi VARCHAR(16), NIK VARCHAR(8), table_dokter VARCHAR(30))

INSERT INTO kode_spesialisasi(kode, spesialisasi, NIK, table_dokter)
	VALUES	('1', 'Dokter Umum', '18104010', 'konsul_umum'),
			('2', 'Dokter Kandungan', '18104018', 'konsul_kehamilan'),
			('3', 'Dokter THT', '18104049', 'konsul_tht')

/*membuat table para dokter*/
CREATE TABLE konsul_umum (PasienId INT, nama VARCHAR(60), gender VARCHAR(24), goldar VARCHAR(2), riwayat VARCHAR(max))

CREATE TABLE konsul_kehamilan (PasienId INT, nama VARCHAR(60), gender VARCHAR(24), goldar VARCHAR(2), riwayat VARCHAR(max))

CREATE TABLE konsul_tht (PasienId INT, nama VARCHAR(60), gender VARCHAR(24), goldar VARCHAR(2), riwayat VARCHAR(max))

/*membuat table record kejadian login dan logout karyawan dan aksi admin*/
CREATE TABLE log_login_karyawan (NIK VARCHAR(8) NOT NULL, nama VARCHAR(30),
waktu DATETIME NOT NULL DEFAULT GETDATE(), keterangan VARCHAR(40))

/*membuat stored prosedur untuk menginputkan record kejadian ke table log_login_karyawan*/
CREATE PROCEDURE sp_AddLogAdmin(@NIK VARCHAR(8), @nama VARCHAR(30), @keterangan VARCHAR(40))
AS
BEGIN
	SET NOCOUNT ON 

	INSERT INTO log_login_karyawan
		(NIK, nama, keterangan)
	VALUES
		(@NIK, @nama, @keterangan)
END

SELECT * FROM log_login_karyawan

/*membuat view untuk memudahkan autentikasi*/
CREATE VIEW view_autentikasi
AS
SELECT data_karyawan.NIK, data_karyawan._password, data_karyawan.jabatan, CONCAT (data_karyawan.nama_a, ' ',data_karyawan.nama_b) AS nama
	FROM data_karyawan

SELECT * FROM view_autentikasi

/*membuat view untuk menampilkan daftar pegawai pada aplikasi*/
CREATE VIEW view_daftar_pegawai
AS
SELECT data_karyawan.NIK, CONCAT (data_karyawan.nama_a, ' ',data_karyawan.nama_b) AS nama , jabatan_karyawan.jabatan, data_karyawan.alamat, data_karyawan.kontak
	FROM data_karyawan
	INNER JOIN jabatan_karyawan ON data_karyawan.jabatan=jabatan_karyawan.kode

SELECT * FROM view_daftar_pegawai

/*membuat view untuk menampilkan daftar dokter spesialis pada aplikasi*/
CREATE VIEW view_daftar_dokter_spesialis
AS
SELECT data_karyawan.NIK, CONCAT (data_karyawan.nama_a, ' ',data_karyawan.nama_b) AS nama , kode_spesialisasi.spesialisasi, kode_spesialisasi.table_dokter
	FROM data_karyawan
	INNER JOIN kode_spesialisasi ON data_karyawan.NIK=kode_spesialisasi.NIK

SELECT * FROM view_daftar_dokter_spesialis

/*membuat fungsi pencarian pada form admin*/
CREATE FUNCTION fx_CariPegawai(@param varchar(20))
RETURNS TABLE AS
RETURN
	SELECT * FROM view_daftar_pegawai
		WHERE NIK = @param OR nama = @param OR jabatan = @param OR nama LIKE ('%'+@param) OR nama LIKE ('%'+@param+'%') OR nama LIKE (@param+'%')

SELECT * FROM fx_CariPegawai('Feb')

/*membuat stored prosedur untuk menginputkan data pasien baru*/
CREATE PROCEDURE sp_AddPatient(@nama_a VARCHAR(30), @nama_b VARCHAR(30), @tempatl VARCHAR(50), @tanggall DATE, @gender VARCHAR(24),
@goldar VARCHAR(2), @alamat VARCHAR(50), @kontak VARCHAR(14), @keperluan VARCHAR(15))
AS
BEGIN
	SET NOCOUNT ON

	INSERT INTO data_pasien
		(nama_a, nama_b, tempat_lahir, tanggal_lahir, gender, goldar, alamat, kontak, Keperluan)
	VALUES
		(@nama_a, @nama_b, @tempatl, @tanggall, @gender, @goldar, @alamat, @kontak, @keperluan)
END

SELECT * FROM data_pasien

SELECT * FROM konsul_umum

EXEC sp_AddPatient 'Mark', 'Zucckegrebeg', 'Sokaraja', '1998-12-12', 'Laki-laki', 'A', 'Jalan Sokaraja', '+6281227063451', '1'

/*membuat view untuk menampilkan daftar pasien pada aplikasi*/
CREATE VIEW view_daftar_pasien
AS
SELECT PasienId, CONCAT (data_pasien.nama_a, ' ',data_pasien.nama_b) AS nama , data_pasien.gender AS Jenis_kelamin, kode_spesialisasi.spesialisasi AS Kunjungan
	FROM data_pasien
	INNER JOIN kode_spesialisasi ON data_pasien.Keperluan=kode_spesialisasi.kode

SELECT * FROM view_daftar_pasien

SELECT * FROM view_daftar_pasien ORDER BY PasienId ASC

/*membuat fungsi pencarian pada form pendaftaran pasien*/
CREATE FUNCTION fx_CariPasien(@param VARCHAR(20))
RETURNS TABLE AS
RETURN
	SELECT * FROM view_daftar_pasien
		WHERE nama = @param OR nama LIKE ('%'+@param) OR nama LIKE ('%'+@param+'%') OR nama LIKE (@param+'%')

SELECT * FROM fx_CariPasien('Zucc')

/*membuat fungsi pencarian pada form dokter*/
CREATE FUNCTION fx_CariPasienDokter(@param VARCHAR(20), @sps VARCHAR(16))
RETURNS TABLE AS
RETURN
	SELECT * FROM view_daftar_pasien
		WHERE nama = @param OR nama LIKE ('%'+@param) OR nama LIKE ('%'+@param+'%') OR nama LIKE (@param+'%') AND Kunjungan LIKE @sps

/*membuat trigger untuk menginputkan data pasien ke database para dokter*/
CREATE TRIGGER tr_specialization
ON data_pasien
AFTER INSERT
AS
BEGIN
	DECLARE @pid INT
	DECLARE @name VARCHAR(60)
	DECLARE @gender VARCHAR(24)
	DECLARE @goldar VARCHAR(2)
	DECLARE @rujuk VARCHAR(20)

	SELECT @pid = PasienId, @name = CONCAT (nama_a, ' ', nama_b), @gender = gender, @goldar = goldar FROM INSERTED

	IF (SELECT Keperluan FROM INSERTED) LIKE '1'
	BEGIN
		INSERT INTO konsul_umum
			(PasienId, nama, gender, goldar)
		VALUES
			(@pid, @name, @gender, @goldar)
	END

	IF (SELECT Keperluan FROM INSERTED) LIKE '2'
	BEGIN
		INSERT INTO konsul_kehamilan
			(PasienId, nama, gender, goldar)
		VALUES
			(@pid, @name, @gender, @goldar)
	END

	IF (SELECT Keperluan FROM INSERTED) LIKE '3'
	BEGIN
		INSERT INTO konsul_tht
			(PasienId, nama, gender, goldar)
		VALUES
			(@pid, @name, @gender, @goldar)
	END
END
