#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, argparse
import json
import plyvel
import logging
from  numba import jit
from flask import Flask, request, Response, jsonify
app = Flask(__name__)
dbName = ''
parser = argparse.ArgumentParser()
parser.add_argument('-db', type=str, default = 'testdb')
parser.add_argument('-port', type=str, default = '8080')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def shutdown_server():
	db.close()
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the werkzeug server.')
	func()

@jit
@app.route('/put', methods=['POST'])
def put():
	reqKey = request.args.get('key')
	reqValue = request.args.get('value')
	r = db.put(bytes(reqKey, 'ascii'), bytes(reqValue, 'ascii'), sync=False)
	if r == None:
		r_data = {
		'status_txt': 'OK',
		'status_code': 200
		}
		return jsonify(r_data)

@jit
@app.route('/get', methods=['GET'])
def get():
	reqKey = request.args.get('key')
	r = db.get(bytes(reqKey, 'ascii'),default=None, verify_checksums=False, fill_cache=True)
	if r == None:
		return Response(
			'{ "status_txt": "NOT_FOUND", "status_code": 404, "data": "" }',
		status=404
		)
	else:
		r_data = {
		'data': r.decode(),
		'status_txt': 'OK',
		'status_code': 200
		}
		return jsonify(r_data)

@jit
@app.route('/delete', methods=['POST'])
def delete():
	reqKey = request.args.get('key')
	r = db.delete(bytes(reqKey, 'ascii'), sync=False)
	if r == None:
		r_data = {
		'status_txt': 'OK',
		'status_code': 200
		}
		return jsonify(r_data)

@jit
@app.route('/queryall', methods=['GET'])
def queryall():
	r = []
	for k,v in db:
		r.append('(' + k.decode() + ', ' + v.decode() + ')')
	r_data = {
		'status_txt': 'OK',
		'status_code': 200,
		'data': r
		}
	return jsonify(r_data)
	
@jit
@app.route('/query', methods=['GET'])
def query():
	reqKey = request.args.get('key')
	r = []
	for k,v in db.iterator(prefix=bytes(reqKey, 'ascii')):
		r.append('(' + k.decode() + ',' + v.decode() + ')')
	r_data = {
		'status_txt': 'OK',
		'status_code': 200,
		'data': r
		}
	return jsonify(r_data)

@jit
@app.route('/getProperty', methods=['GET'])
def get_property():
	reqName = bytes(request.args.get('name'), 'ascii')
	result = db.get_property(reqName)
	return result.decode()


@app.route('/shutdown', methods=['POST'])
def shutdown():
	shutdown_server()
	return 'Server shutting down...\n'

if __name__ =='__main__':
	args = parser.parse_args()
	dbName = args.db
	
	db = plyvel.DB('./dbs/'+dbName, \
	create_if_missing=True, \
	error_if_exists=False, \
	paranoid_checks=False, \
	write_buffer_size=4*1024*1024, \
	max_open_files=1000, \
	lru_cache_size=100000, \
	block_size=4*1024, \
	block_restart_interval=16, \
	max_file_size=2*1024*1024, \
	compression='snappy', \
	bloom_filter_bits=10)
	
	app.run(host='0.0.0.0', port=int(args.port))