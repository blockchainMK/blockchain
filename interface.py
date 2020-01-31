from flask import Flask, request, render_template, session, flash, redirect
from backOffice import json, cx_Oracle, listUniversitas, addUniversitas, listKota, listProvinsi, addProvinsi, addKota
from frontOffice import json, hashlib, cx_Oracle, login_, add_user, print_blockchain, add_add_data, detail_data
import os


app = Flask(__name__)
app.secret_key = "backOffice"
app.config["IMAGE_UPLOADS"] = "/Users/masasih/Sites/Program/blockchain/static/uploads"

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'GET' :
		return render_template('login.html')
	if request.method == 'POST' :
		username = str(request.form.get('username'))
		password = str(request.form.get('password'))

		user = login_(username, password)

		if user==[]:
			flash('*Invalid username or password. Please try again!', 'error')
			return redirect('/')
		elif user[0][1]==username and user[0][2]==password:
			session['username'] = username
			if user[0][1]=='Administrator':
				# return render_template('home.html', blockchain=blockchain)
				return redirect('/homeAdmin')
			else:
				return redirect('/home')
		else:
			flash('*Invalid username or password. Please try again!', 'error')
			return redirect('/')
		# return render_template('test.html', user=user)


@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'GET' :
		return render_template('register.html')
	if request.method == 'POST' :
		username = str(request.form.get('username'))
		password = str(request.form.get('password'))
		message = add_user(username, password)
		if message==1:
			flash('Your registration was successful.', 'success')
			return redirect('/')
		else:
			flash('Username has been registered. Choose other username.', 'error')
			return redirect('/register')


@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/')


@app.route('/homeAdmin', methods=['GET'])
def homeAdmin():
	if 'username' in session:
		if session['username']=='Administrator':
			return render_template('homeAdmin.html')
		else:
			flash('You are not an administrator!')
			return redirect('/')
	else:
		return redirect('/')


@app.route('/conCollege', methods=['GET','POST'])
def conCollege():
	if 'username' in session:
		if session['username']=='Administrator':
			if request.method == 'GET' :
				dataCollege = listUniversitas()
				return render_template('conCollege.html', dataCollege=dataCollege)
			if request.method == 'POST' :
				collegeName = str(request.form.get('collegeName'))

				addUniversitas(collegeName)
				flash('College data added successfully.', 'success')
				return redirect('/conCollege')
		else:
			flash('You are not an administrator!')
			return redirect('/')
	else:
		return redirect('/')


@app.route('/conArea', methods=['GET'])
def conArea():
	if 'username' in session:
		if session['username']=='Administrator':
			dataProvince = listProvinsi()
			dataCity = listKota()
			return render_template('conArea.html', dataProvince=dataProvince, dataCity=dataCity)
		else:
			flash('You are not an administrator!')
			return redirect('/')
	else:
		return redirect('/')

@app.route('/addProvince', methods=['POST'])
def addProvince():
	if 'username' in session:
		if session['username']=='Administrator':
			provinceName = str(request.form.get('provinceName'))
			addProvinsi(provinceName)
			flash('Province data added successfully.', 'success')

			return redirect('/conArea')
		else:
			flash('You are not an administrator!')
			return redirect('/')
	else:
		return redirect('/')

@app.route('/addCity', methods=['POST'])
def addCity():
	if 'username' in session:
		if session['username']=='Administrator':
			provinceName = str(request.form.get('provinceName1'))
			cityName = str(request.form.get('cityName'))
			addKota(provinceName, cityName)
			flash('District data added successfully.', 'success')

			return redirect('/conArea')
		else:
			flash('You are not an administrator!')
			return redirect('/')
	else:
		return redirect('/')


@app.route('/home', methods=['GET'])
def home():
	if 'username' in session:
		blockchain = print_blockchain()
		return render_template('home.html', blockchain=blockchain)
	else:
		# return '<p>Please login first</p>'
		return redirect('/')


@app.route('/addData', methods=['GET','POST'])
def add():
	if 'username' in session:
		if request.method == 'GET' :
			dataCollege = listUniversitas()
			dataProvince = listProvinsi()
			dataCity = listKota()
			return render_template('add.html', dataCollege=dataCollege, dataProvince=dataProvince, dataCity=dataCity)
		if request.method == 'POST' :
			gelar1 = str(request.form.get('gelar1'))
			nama = str(request.form.get('nama'))
			gelar2 = str(request.form.get('gelar2'))
			ttl1 = str(request.form.get('ttl1'))
			ttl2 = str(request.form.get('ttl2'))
			ttl = ttl1+', '+ttl2
			univ = str(request.form.get('univ'))
			nomor = str(request.form.get('nomor'))
			tanggal = str(request.form.get('tanggal'))
			tahun = str(request.form.get('tahun'))
			
			image = request.files['filenya']
			filename, file_extension = os.path.splitext(image.filename)
			rename_filename = nomor.replace('/', '-')
			image.save(os.path.join(app.config['IMAGE_UPLOADS'], rename_filename+file_extension))

			# data_transaction = { "gelar1":gelar1, "nama":nama, "gelar2":gelar2, "ttl":ttl, "univ":univ, "nomor":nomor, "tanggal":tanggal, "tahun":tahun }
			# a = json.dumps(data_transaction)

			add_add_data(session['username'], gelar1, nama, gelar2, ttl, univ, nomor, tanggal, tahun, rename_filename+file_extension)
			flash('Data added successfully.', 'success')
			return redirect('/addData')
	else:
		return redirect('/')


@app.route('/detailData/<operand>', methods=['GET'])
def detail(operand):
	if 'username' in session:
		data = detail_data(operand)
		return render_template('detail.html', data=data)
	else:
		return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
