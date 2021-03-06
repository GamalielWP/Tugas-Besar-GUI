USE [master]
GO
/****** Object:  Database [db_puskesmas]    Script Date: 7/9/2020 7:21:14 AM ******/
CREATE DATABASE [db_puskesmas]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'db_puskesmas', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\DATA\db_puskesmas.mdf' , SIZE = 3136KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'db_puskesmas_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL11.SQLEXPRESS\MSSQL\DATA\db_puskesmas_log.ldf' , SIZE = 832KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO
ALTER DATABASE [db_puskesmas] SET COMPATIBILITY_LEVEL = 110
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [db_puskesmas].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [db_puskesmas] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [db_puskesmas] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [db_puskesmas] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [db_puskesmas] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [db_puskesmas] SET ARITHABORT OFF 
GO
ALTER DATABASE [db_puskesmas] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [db_puskesmas] SET AUTO_CREATE_STATISTICS ON 
GO
ALTER DATABASE [db_puskesmas] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [db_puskesmas] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [db_puskesmas] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [db_puskesmas] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [db_puskesmas] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [db_puskesmas] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [db_puskesmas] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [db_puskesmas] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [db_puskesmas] SET  ENABLE_BROKER 
GO
ALTER DATABASE [db_puskesmas] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [db_puskesmas] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [db_puskesmas] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [db_puskesmas] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [db_puskesmas] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [db_puskesmas] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [db_puskesmas] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [db_puskesmas] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [db_puskesmas] SET  MULTI_USER 
GO
ALTER DATABASE [db_puskesmas] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [db_puskesmas] SET DB_CHAINING OFF 
GO
ALTER DATABASE [db_puskesmas] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [db_puskesmas] SET TARGET_RECOVERY_TIME = 0 SECONDS 
GO
USE [db_puskesmas]
GO
/****** Object:  StoredProcedure [dbo].[sp_AddLogAdmin]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_AddLogAdmin](@NIK VARCHAR(8), @nama VARCHAR(30), @keterangan VARCHAR(40))
AS
BEGIN
	SET NOCOUNT ON 

	INSERT INTO log_login_karyawan
		(NIK, nama, keterangan)
	VALUES
		(@NIK, @nama, @keterangan)
END
GO
/****** Object:  StoredProcedure [dbo].[sp_AddPatient]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[sp_AddPatient](@nama_a VARCHAR(30), @nama_b VARCHAR(30), @tempatl VARCHAR(50), @tanggall DATE, @gender VARCHAR(24),
@goldar VARCHAR(2), @alamat VARCHAR(50), @kontak VARCHAR(14), @keperluan VARCHAR(15))
AS
BEGIN
	SET NOCOUNT ON

	INSERT INTO data_pasien
		(nama_a, nama_b, tempat_lahir, tanggal_lahir, gender, goldar, alamat, kontak, Keperluan)
	VALUES
		(@nama_a, @nama_b, @tempatl, @tanggall, @gender, @goldar, @alamat, @kontak, @keperluan)
END
GO
/****** Object:  Table [dbo].[data_karyawan]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[data_karyawan](
	[NIK] [varchar](8) NOT NULL,
	[_password] [varchar](20) NOT NULL,
	[jabatan] [varchar](3) NULL,
	[nama_a] [varchar](30) NULL,
	[nama_b] [varchar](30) NULL,
	[alamat] [varchar](50) NULL,
	[kontak] [varchar](14) NULL,
PRIMARY KEY CLUSTERED 
(
	[NIK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[data_pasien]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[data_pasien](
	[PasienId] [int] IDENTITY(1,1) NOT NULL,
	[nama_a] [varchar](30) NULL,
	[nama_b] [varchar](30) NULL,
	[tempat_lahir] [varchar](50) NULL,
	[tanggal_lahir] [date] NULL,
	[gender] [varchar](24) NOT NULL,
	[goldar] [varchar](2) NOT NULL,
	[alamat] [varchar](50) NULL,
	[kontak] [varchar](14) NULL,
	[Keperluan] [varchar](1) NOT NULL
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[jabatan_karyawan]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[jabatan_karyawan](
	[kode] [varchar](3) NULL,
	[jabatan] [varchar](10) NULL
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[kode_spesialisasi]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[kode_spesialisasi](
	[kode] [varchar](1) NULL,
	[spesialisasi] [varchar](16) NULL,
	[NIK] [varchar](8) NULL,
	[table_dokter] [varchar](30) NULL
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[konsul_kehamilan]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[konsul_kehamilan](
	[PasienId] [int] NULL,
	[nama] [varchar](60) NULL,
	[gender] [varchar](24) NULL,
	[goldar] [varchar](2) NULL,
	[riwayat] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[konsul_tht]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[konsul_tht](
	[PasienId] [int] NULL,
	[nama] [varchar](60) NULL,
	[gender] [varchar](24) NULL,
	[goldar] [varchar](2) NULL,
	[riwayat] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[konsul_umum]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[konsul_umum](
	[PasienId] [int] NULL,
	[nama] [varchar](60) NULL,
	[gender] [varchar](24) NULL,
	[goldar] [varchar](2) NULL,
	[riwayat] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[log_data_pasien]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[log_data_pasien](
	[NIK] [varchar](8) NOT NULL,
	[nama] [varchar](30) NULL,
	[waktu] [datetime] NOT NULL,
	[keterangan] [varchar](40) NULL
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  Table [dbo].[log_login_karyawan]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
SET ANSI_PADDING ON
GO
CREATE TABLE [dbo].[log_login_karyawan](
	[NIK] [varchar](8) NOT NULL,
	[nama] [varchar](30) NULL,
	[waktu] [datetime] NOT NULL,
	[keterangan] [varchar](40) NULL
) ON [PRIMARY]

GO
SET ANSI_PADDING OFF
GO
/****** Object:  View [dbo].[view_daftar_pasien]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[view_daftar_pasien]
AS
SELECT PasienId, CONCAT (data_pasien.nama_a, ' ',data_pasien.nama_b) AS nama , data_pasien.gender AS Jenis_kelamin, kode_spesialisasi.spesialisasi AS Kunjungan
	FROM data_pasien
	INNER JOIN kode_spesialisasi ON data_pasien.Keperluan=kode_spesialisasi.kode
GO
/****** Object:  UserDefinedFunction [dbo].[fx_CariPasienDokter]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[fx_CariPasienDokter](@param VARCHAR(20), @sps VARCHAR(16))
RETURNS TABLE AS
RETURN
	SELECT * FROM view_daftar_pasien
		WHERE nama = @param OR nama LIKE ('%'+@param) OR nama LIKE ('%'+@param+'%') OR nama LIKE (@param+'%') AND Kunjungan LIKE @sps
GO
/****** Object:  View [dbo].[view_daftar_pegawai]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[view_daftar_pegawai]
AS
SELECT data_karyawan.NIK, CONCAT (data_karyawan.nama_a, ' ',data_karyawan.nama_b) AS nama , jabatan_karyawan.jabatan, data_karyawan.alamat, data_karyawan.kontak
	FROM data_karyawan
	INNER JOIN jabatan_karyawan ON data_karyawan.jabatan=jabatan_karyawan.kode
GO
/****** Object:  UserDefinedFunction [dbo].[fx_CariPegawai]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[fx_CariPegawai](@param varchar(20))
RETURNS TABLE AS
RETURN
	SELECT * FROM view_daftar_pegawai
		WHERE NIK = @param OR nama = @param OR jabatan = @param OR nama LIKE ('%'+@param) OR nama LIKE ('%'+@param+'%') OR nama LIKE (@param+'%')
GO
/****** Object:  UserDefinedFunction [dbo].[fx_CariPasien]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE FUNCTION [dbo].[fx_CariPasien](@param varchar(20))
RETURNS TABLE AS
RETURN
	SELECT * FROM view_daftar_pasien
		WHERE nama = @param OR nama LIKE ('%'+@param) OR nama LIKE ('%'+@param+'%') OR nama LIKE (@param+'%')
GO
/****** Object:  View [dbo].[view_autentikasi]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[view_autentikasi]
AS
SELECT data_karyawan.NIK, data_karyawan._password, data_karyawan.jabatan, CONCAT (data_karyawan.nama_a, ' ',data_karyawan.nama_b) AS nama
	FROM data_karyawan
GO
/****** Object:  View [dbo].[view_daftar_dokter_spesialis]    Script Date: 7/9/2020 7:21:14 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE VIEW [dbo].[view_daftar_dokter_spesialis]
AS
SELECT data_karyawan.NIK, CONCAT (data_karyawan.nama_a, ' ',data_karyawan.nama_b) AS nama , kode_spesialisasi.spesialisasi, kode_spesialisasi.table_dokter
	FROM data_karyawan
	INNER JOIN kode_spesialisasi ON data_karyawan.NIK=kode_spesialisasi.NIK
GO
ALTER TABLE [dbo].[log_data_pasien] ADD  DEFAULT (getdate()) FOR [waktu]
GO
ALTER TABLE [dbo].[log_login_karyawan] ADD  DEFAULT (getdate()) FOR [waktu]
GO
ALTER TABLE [dbo].[data_pasien]  WITH CHECK ADD CHECK  (([gender]='Apache Attack Helicopter' OR [gender]='Perempuan' OR [gender]='Laki-laki'))
GO
ALTER TABLE [dbo].[data_pasien]  WITH CHECK ADD CHECK  (([goldar]='O' OR [goldar]='AB' OR [goldar]='B' OR [goldar]='A'))
GO
ALTER TABLE [dbo].[data_pasien]  WITH CHECK ADD CHECK  (([keperluan]='3' OR [keperluan]='2' OR [keperluan]='1'))
GO
USE [master]
GO
ALTER DATABASE [db_puskesmas] SET  READ_WRITE 
GO
