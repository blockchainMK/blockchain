import json
import cx_Oracle

#  Membuat koneksi python dnegan oracle
connect = cx_Oracle.connect('eka/eka@service1')

def addUniversitas(name):
	cursor = connect.cursor()
	statement = 'insert into universitas(nama_universitas) values (:name)'
	cursor.execute(statement, {'name':name})
	connect.commit()

def listUniversitas():
	cursor = connect.cursor()
	statement = 'select * from universitas order by nama_universitas'
	dataUniversity = cursor.execute(statement).fetchall()
	return dataUniversity


def addProvinsi(name):
	cursor = connect.cursor()
	statement = 'insert into provinsi(nama_provinsi) values (:name)'
	cursor.execute(statement, {'name':name})
	connect.commit()

def listProvinsi():
	cursor = connect.cursor()
	statement = 'select * from provinsi order by nama_provinsi'
	dataProvince = cursor.execute(statement).fetchall()
	return dataProvince


def addKota(province, city):
	cursor = connect.cursor()
	statement = 'insert into kota(id_provinsi, nama_kota) values (:province, :name)'
	cursor.execute(statement, {'province':province, 'name':city})
	connect.commit()

def listKota():
	cursor = connect.cursor()
	statement = 'select * from kota order by nama_kota'
	dataCity = cursor.execute(statement).fetchall()
	return dataCity


def login_(username, password):
	cursor = connect.cursor()
	statement = 'select * from po_user_and_pass where user_name = :username and password = :password'
	user = cursor.execute(statement, {'username':username, 'password':password}).fetchall()
	return user
