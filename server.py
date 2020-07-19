#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, argparse
import json
import plyvel
from flask import Flask, request, Response
app = Flask(__name__)
dbName = ''
parser = argparse.ArgumentParser()
parser.add_argument('-db', type=str, default = 'testdb')
parser.add_argument('-port', type=str, default = '8888')

@app.route('/put', methods=['POST'])
def put():
	data = json.loads(request.get_data().decode())
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = db.put(bytes(data['key'], 'ascii'), bytes(data['value'], 'ascii'))
	db.close()
	if r == None:
		r_data = {
		'status': 'OK'
		}
		return Response(json.dumps(r_data), status=200)

@app.route('/get', methods=['GET'])
def get():
	data = json.loads(request.get_data().decode())
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = db.get(bytes(data['key'], 'ascii'))
	db.close()
	r_data = {
		'status': 'OK',
		'data': '(' + data['key'] + ',' + r.decode() + ')'
		}
	return Response(json.dumps(r_data), status=200)

@app.route('/delete', methods=['POST'])
def delete():
	data = json.loads(request.get_data().decode())
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = db.delete(bytes(data['key'], 'ascii'))
	db.close()
	if r == None:
		r_data = {
		'status': 'OK'
		}
		return Response(json.dumps(r_data), status=200)

@app.route('/queryall', methods=['GET'])
def queryall():
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = []
	for k,v in db:
		r.append('(' + k.decode() + ',' + v.decode() + ')')
	db.close()
	r_data = {
		'status': 'OK',
		'data': r
		}
	return Response(json.dumps(r_data), status=200)

@app.route('/query', methods=['GET'])
def query():
	data = json.loads(request.get_data().decode())
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = []
	for k,v in db.iterator(prefix=bytes(data['key'], 'ascii')):
		r.append('(' + k.decode() + ',' + v.decode() + ')')
	db.close()
	r_data = {
		'status': 'OK',
		'data': r
		}
	return Response(json.dumps(r_data), status=200)


if __name__ =='__main__':
	global dbName
	args = parser.parse_args()
	dbName = args.db
	app.run(host='0.0.0.0', debug=True, port=int(args.port))