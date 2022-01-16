import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
		
@app.route('/inventory/add', methods=['POST'])
def add_inventory():
	try:
		_json = request.json
		_Typ = _json['Typ']
		_Hersteller = _json['Hersteller']
		_Model = _json['Model']
		_Seriennummer = _json['Seriennummer']
		_UserId = _json['UserId']
		if _Typ and _Hersteller and _Model and _Seriennummer and _UserId and request.method == 'POST':
			sql = "INSERT INTO inventory(Typ, Hersteller, Model, Seriennummer, UserId) VALUES(%s, %s, %s, %s, %s)"
			data = (_Typ, _Hersteller, _Model, _Seriennummer, _UserId)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Inventar eingetragen!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/employees/add', methods=['POST'])
def add_employees():
	try:
		_json = request.json
		_Vorname = _json['Vorname']
		_Nachname = _json['Nachname']
		_Email = _json['Email']
		_Telefon = _json['Telefon']
		if _Vorname and _Nachname and _Email and _Telefon and request.method == 'POST':
			sql = "INSERT INTO employees(Vorname, Nachname, Email, Telefon) VALUES(%s, %s, %s, %s)"
			data = (_Vorname, _Nachname, _Email, _Telefon)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('Mitarbeiter eingetragen!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/inventory')
def inventory():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM inventory")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
	
@app.route('/employees')
def employees():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM employees")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/inventory/<int:id>')
def inventar(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM inventory WHERE Id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/employees/<int:id>')
def employee(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM employees WHERE Id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/inventory/delete/<int:id>')
def delete_inventory(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM inventory WHERE Id=%s", (id,))
		conn.commit()
		resp = jsonify('Inventar entfernt!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()	

@app.route('/employees/delete/<int:id>')
def delete_employee(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM employees WHERE Id=%s", (id,))
		conn.commit()
		resp = jsonify('Mitarbeiter entfernt!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404    

    return resp
		
if __name__ == "__main__":
    app.run()
