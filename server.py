#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, argparse
import json
import plyvel
from flask import Flask, request, Response, jsonify
app = Flask(__name__)
dbName = ''
parser = argparse.ArgumentParser()
parser.add_argument('-db', type=str, default = 'testdb')
parser.add_argument('-port', type=str, default = '8888')

@app.route('/put', methods=['POST'])
def put():
	reqKey = request.args.get('key')
	reqValue = request.args.get('value')
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = db.put(bytes(reqKey, 'ascii'), bytes(reqValue, 'ascii'))
	db.close()
	if r == None:
		r_data = {
		'status': 'OK'
		}
		return jsonify(r_data)

@app.route('/get', methods=['GET'])
def get():
	reqKey = request.args.get('key')
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = db.get(bytes(reqKey, 'ascii'))
	db.close()
	r_data = {
		'status': 'OK',
		'data': '(' + reqKey + ', ' + r.decode() + ')'
		}
	return jsonify(r_data)

@app.route('/delete', methods=['POST'])
def delete():
	reqKey = request.args.get('key')
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = db.delete(bytes(reqKey, 'ascii'))
	db.close()
	if r == None:
		r_data = {
		'status': 'OK'
		}
		return jsonify(r_data)

@app.route('/queryall', methods=['GET'])
def queryall():
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = []
	for k,v in db:
		r.append('(' + k.decode() + ', ' + v.decode() + ')')
	db.close()
	r_data = {
		'status': 'OK',
		'data': r
		}
	return jsonify(r_data)

@app.route('/query', methods=['GET'])
def query():
	reqKey = request.args.get('key')
	db = plyvel.DB('./dbs/'+dbName, create_if_missing=True)
	r = []
	for k,v in db.iterator(prefix=bytes(reqKey, 'ascii')):
		r.append('(' + k.decode() + ',' + v.decode() + ')')
	db.close()
	r_data = {
		'status': 'OK',
		'data': r
		}
	return jsonify(r_data)


if __name__ =='__main__':
	global dbName
	args = parser.parse_args()
	dbName = args.db
	app.run(host='0.0.0.0', debug=True, port=int(args.port))