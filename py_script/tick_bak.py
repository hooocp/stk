#!/usr/bin/python
#coding:utf8


import os
import csv
import re

class tick(object):
	def __init__(self,input_csv):
		self.tick=input_csv
	def receive_path_name(self,tick):  #将所有文件路径及名称存入数组内
		self.filesname=[]
		for root,dirs,files in os.walk(self.tick):
			for file_name in files:
				self.filesname.append(os.path.join())
		
	def csv_funct(self,filesname):
		a=[]
		b=[]
		for fl in self.filesname:
			b=re.split('[\/\.]',fl)
			csv_writer=csv.writer(file(fl,'wb'))
			for line in csv_writer:
				csv_writer.writerow([line,b[-1],b[-2]])
			




if __name__=='__main__':
	a=raw_input('plese input the path:')
	c=tick(a)
	c.csv_funct(c.filesname)
