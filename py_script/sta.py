import multiprocessing as mp
import time

def seq(count):
    print "runing seq"
    start_time = time.time()
    result = []
    for i in range(count):
        result.append(cube(i))
    print "seq --- time:{0:.4f}".format(time.time() - start_time)
    #print "seq --- time:{0:.4f}, result:{1}".format(time.time() - start_time, result)
    print result

def par(count):
    print "runing par"
    start_time = time.time()
    result = mp.Pool(processes=8).map(cube,range(count))
    print "par --- time:{0:.4f}".format(time.time() - start_time)
    #print "par --- time:{0:.4f}, result:{1}".format(time.time() - start_time, result)
    print result
def cube(x):
    return ((x*x*x*x)**100000)%9

if __name__ == "__main__":    
    count = 400
  #  seq(count)
    par(count)
