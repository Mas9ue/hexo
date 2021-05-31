# -*- coding: utf-8 -*-

from gevent import monkey
monkey.patch_all()
import argparse
import redis
import gevent
from gevent import pool
import threading

lock = threading.Lock()

def WriteFile(filename,result):
    f = open(filename,'a+')
    f.write(result)
    f.close


def redis_ana(ip):
	try:
		r = redis.Redis(host=ip, port=6379, decode_responses=True)
		r.info()
		WriteFile("record.txt",ip + '\tredis avaliable\n')
	except Exception as e:
		return


def redis_check(ip_path):
	threads = []
	global pool
	pool = pool.Pool(20)
	filehandler = open(ip_path,'r')
	line = filehandler.readline()
	if line.endswith('\n'):
		line = line[0:-1]

	while(line):
		threads.append(pool.spawn(redis_ana,line))
		line = filehandler.readline()
		if line.endswith('\n'):
			line = line[0:-1]
	
	gevent.joinall(threads)
	filehandler.close()






if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-l","--ip_list",help="ip_list",type=str)
	args = parser.parse_args()

	ip_list = args.ip_list
	redis_check(ip_list)






