import hashlib
import json
from datetime import datetime
import cx_Oracle

#  Membuat koneksi python dnegan oracle
connect = cx_Oracle.connect('eka/eka@service1')

fee = float(10)
open_data = []  # menyimpan data transaksi sementara

# Membuat block genesis
genesis_block = {'Index': 0,
                 'Nonce': 30,
                 'Waktu': str(datetime.now()),
                 'Previous Hash': '0000000000000000000000000000000000000000000000000000000000000000',
                 'Data Penyimpanan': []
                 }

blockchain = [genesis_block]


# melakukan proses hashing
def hashing(block):
    return hashlib.sha256(json.dumps(block).encode()).hexdigest()


# memvalidasi hash data
def valid_proof(input_data, last_hash, nonce):
    exp = (str(input_data) + str(last_hash) + str(nonce)).encode()
    guess_hash = hashlib.sha256(exp).hexdigest()
    return guess_hash[0:2] == '30'


# membuat nonce dari suatu proses hashing
def pow_nonce():
    last_block = blockchain[-1]
    last_hash = hashing(last_block)
    nonce = 0
    while not valid_proof(open_data, last_hash, nonce):
        nonce += 1
    return nonce


# memperoleh block terakhir dalam blockchain
def get_last_value():
    return blockchain[-1]


# menambah data
def add_data(pengirim, in_data):
    transaction = {'Pemilik': pengirim, 'Penyimpan': 'MK', 'Data Ijazah': in_data}
    open_data.append(transaction)


# melakukan proses mining
def mine_block():
    last_block = blockchain[-1]
    hashed_block = hashing(last_block)
    nonce = pow_nonce()
    reward_transaction = {'Pengirim': 'MK', 'Penerima': 'Miners', 'Jumlah': fee}
    open_data.insert(0, reward_transaction)
    block = {'Index': len(blockchain),
             'Nonce': nonce,
             'Waktu': str(datetime.now()),
             'Previous Hash': hashed_block,
             'Data Penyimpanan': open_data
             }
    blockchain.append(block)


# memperoleh hasil dari input
def get_data(gelar1, nama, gelar2, ttl, univ, nomor, tanggal, tahun, filename):
    return gelar1, nama, gelar2, ttl, univ, nomor, tanggal, tahun, filename


def print_blockchain():
	cursor = connect.cursor()
	statement = 'select * from po_blockchain order by index_block'
	blockchain = cursor.execute(statement).fetchall()
	return blockchain


def detail_data(index):
	cursor = connect.cursor()
	statement = 'select * from po_user_data where id_data='+index
	data = cursor.execute(statement).fetchall()
	return data


def add_user(username, password):
	cursor1 = connect.cursor()
	statement1 = 'select user_name from po_user_and_pass where user_name = :username'
	connectdition = cursor1.execute(statement1, {'username':username}).fetchall()
	if connectdition==[]:
		cursor2 = connect.cursor()
		statement2 = 'insert into po_user_and_pass(user_name, password) values (:username, :password)'
		cursor2.execute(statement2, {'username':username, 'password':password})
		connect.commit()
		message = 1
	else:
		message = 2
	return message


def login_(username, password):
	cursor = connect.cursor()
	statement = 'select * from po_user_and_pass where user_name = :username and password = :password'
	user = cursor.execute(statement, {'username':username, 'password':password}).fetchall()
	return user


def add_add_data(username, gelar1, nama, gelar2, ttl, univ, nomor, tanggal, tahun, filename):
	tx_data = get_data(gelar1, nama, gelar2, ttl, univ, nomor, tanggal, tahun, filename)
	add_data(username, tx_data)

	# filename_ = '/Users/masasih/Sites/Program/blockchain/static/uploads/' + filename;

	cursor1 = connect.cursor()
	statement1 = 'insert into po_user_data(username, gelar_depan, nama, gelar_belakang, ttl, univ, no_ijazah, tgl_ijazah, thn_ijazah, scan_file) values (:username, :gelar1, :nama, :gelar2, :ttl, :univ, :nomor, :tanggal, :tahun, :file_)'
	cursor1.execute(statement1, {'username':username, 'gelar1':gelar1, 'nama':nama, 'gelar2':gelar2, 'ttl':ttl, 'univ':univ, 'nomor':nomor, 'tanggal':tanggal, 'tahun':tahun, 'file_':filename})
	connect.commit()

	mine_block()

	cursor2 = connect.cursor()
	statement2 = 'insert into po_blockchain(nonce, timestamp, username, previous_hash) values (:2, :3, :4, :5)'
	cursor2.execute(statement2, (blockchain[-1]['Nonce'], blockchain[-1]['Waktu'], username, blockchain[-1]['Previous Hash']))
	connect.commit()


def listUniversitas():
	cursor = connect.cursor()
	statement = 'select * from universitas order by nama_universitas'
	dataUniversity = cursor.execute(statement).fetchall()
	return dataUniversity


def listProvinsi():
	cursor = connect.cursor()
	statement = 'select * from provinsi order by nama_provinsi'
	dataProvince = cursor.execute(statement).fetchall()
	return dataProvince


def listKota():
	cursor = connect.cursor()
	statement = 'select * from kota order by nama_kota'
	dataCity = cursor.execute(statement).fetchall()
	return dataCity
