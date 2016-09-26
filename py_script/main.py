# -*- coding: utf-8 -*-
from urllib import request
import time
import multiprocessing as mlp
import logging
import os
import codecs


def decorator(func_input):
    def inner_funct(*args, **kwargs):
        print('begin at ', time.ctime())
        result = func_input(*args, **kwargs)
        print('stop at ', time.ctime())
        return result
    return inner_funct


def callbackfunc(blocknum, blocksize, totalsize):
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print("%.2f" % percent)


def walk_dir(dir_path, topdown=True, return_flag=0):
    dir_files = []
    dir_dirs = []
    for root, dirs, files in os.walk(dir_path, topdown):
        for name in files:
            dir_files.append(os.path.join(root, name))
        for name in dirs:
            dir_dirs.append(os.path.join(root, name))
    if return_flag == 0:
        return dir_files
    return dir_dirs


@decorator
def download(stock_list, trd_date):
    left_stock = []
    counter = 0
    new_path = os.getcwd() + '/stock_temp' + trd_date
    try:
        os.mkdir(new_path)
    except FileExistsError:
        pass
    for stock_id in stock_list:
        counter += 1
        url = 'http://market.finance.sina.com.cn/downxls.php?date={trd_date}&symbol={stock_id}'
        file_name = new_path + '/{trd_date}_{stock_id}.csv'.format(trd_date=trd_date, stock_id=stock_id)
        try:
            request.urlretrieve(url.format(trd_date=trd_date, stock_id=stock_id), file_name, callbackfunc)
        except:
            print('Http Error ', counter)
            left_stock.append(stock_id)
            continue
        with codecs.open(file_name, 'r', 'gbk') as f:
            line1 = f.readline(7)
        if 'script' in line1:
            os.system('rm -f {files}'.format(files=file_name))
    print('Loop finished')
    print(left_stock)
    return left_stock


def csv_process(files_path, trd_date):
    for file_name in range(len(files_path)):
        fl_name = file_name.split('/')[-1]
        cmd1 = 'LANG=C sed -i {dot}{dot} s/^/{fl_name},/g {ab_path_file_name} '.format(fl_name=fl_name.split('.')[0],
                                                                           ab_path_file_name=file_name, dot="'")
        os.system(cmd1)
        cmd2 = 'LANG=C sed -i {dot}{dot} 1d {ab_path_file_name} '.format(fl_name=fl_name.split('.')[0],
                                                                                       ab_path_file_name=file_name,
                                                                                       dot="'")
        os.system(cmd2)

    os.chdir(os.getcwd()+'/stock_temp' + trd_date)
    os.system('cat *.csv > all.csv')
    print('Changed to csv file')


def save_to_db(file_name='input.csv', host='localhost', user='user', password='passwd', db='db', port=1366):
    import pymysql
    conn = pymysql.connect(host='localhost',
                           user='user',
                           password='passwd',
                           db='db',
                           port=1366,
                           cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()


def data_verification():
    pass


def yield_stock_id():
    stock_id_header = {'600': 'sh', '601': 'sh', '000': 'sz', '002': 'sz', '300': 'sz'}
    stocklist = []
    for i in range(1000):
        for key in stock_id_header:
            stocklist.append(stock_id_header[key] + key + str(i).zfill(3))
    return stocklist


if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.DEBUG)
    logging.debug('this is a message')
    today_date = time.strftime('%Y-%m-%d')
    stock_list = yield_stock_id()
    left_stocks = download(stock_list, today_date)
    while True:
        print('stock_lf: ', len(left_stocks))
        if len(left_stocks) == 0:
            break
        left_stocks = download(left_stocks, today_date)
    file_paths = walk_dir(os.getcwd())
    csv_process(file_paths, today_date)
    


