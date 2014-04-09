#!/usr/bin/env python
from itertools import izip, islice
from operator import methodcaller
import numpy as np
import matplotlib
matplotlib.use('Agg') # use backend that does not plot to user
from coroutine import coroutine
import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from mpl_toolkits.mplot3d import Axes3D
# from mpl_toolkits.mplot3d.art3d import juggle_axes
import time
import matplotlib.cm as cm
# fig = plt.figure()
# ax = fig.add_axes([0, 0, 1, 1], projection='3d')
# FLOOR = -15
# CEILING = 15
# ax.set_xlim3d(FLOOR,CEILING)
# ax.set_ylim3d(FLOOR,CEILING)
# ax.set_zlim3d(FLOOR,CEILING)
# scat = ax.scatter([],[],[],animated=True)
# plt.ion() # turn on interactive
plt.ioff()
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
# colors = iter(cm.rainbow(np.linspace(0,1,60000)))
# colors = itertools.cycle(["r", "b", "g"])
# colors = iter(cm.rainbow(np.linspace(0,1,6)))

def read_in_chunk(input_file, chunk_size=20):
     while True:
         next_n_lines = list(islice(input_file,chunk_size))
         if not next_n_lines:
              break
         yield next_n_lines
def data_stream(target):
    with open(r'./coup_rank.out') as coup:
       with open(r'./gap_rank.out') as gap:
          with open(r'./main.qc.xyz') as xyz:
		for (b1,b2,b3) in izip(read_in_chunk(coup),read_in_chunk(gap),read_in_chunk(xyz,503)):
                     target.send([b1,b2,b3])

distance_x_y = lambda x : (((x[0]-x[1])**2).sum())**0.5

@coroutine
def filter(sink):
    #print "start receive"
    while True:
        [b1,b2,b3] = (yield)
        # print b1,b2,b3
        coup_rank = [x.split()[1] for x in b1]
        gap_rank = [x.split()[1] for x in b2]
        xyz_list = [x.split() for x in b3]
        xyz_list.pop(0) # remove first two text header
        del xyz_list[0]
        map(methodcaller("pop",0),xyz_list)
        xyz_list = [map(float,xyz) for xyz in xyz_list]
	from IPython.core.debugger import Tracer; breakpoint1 = Tracer()
	point1 = xyz_list[0]
	point2 = xyz_list[1]
	#print point1,point2
	zero_point = [(x+y)/2 for (x,y) in zip(point1,point2)] 
	#print zero_point
        #print coup_rank,gap_rank
        coup_rank = map(int,coup_rank)
        gap_rank = map(int,gap_rank)
        #print coup_rank,gap_rank
        xyz_list_gap = [xyz_list[x-1] for x in gap_rank]
        xyz_list_coup = [xyz_list[x-1] for x in coup_rank]
        #xyz_list_gap.insert(0,xyz_list[0])
        #xyz_list_coup.insert(0,xyz_list[0])
        #print coup_rank,gap_rank,xyz_list_gap,xyz_list_coup
        in_coup_not_gap_set = set(coup_rank).difference(set(gap_rank))
        in_gap_not_coup_set = set(gap_rank).difference(set(coup_rank))
        #in_coup_not_gap_list.append(list(in_coup_not_gap_set))
        #in_gap_not_coup_list.append(list(in_gap_not_coup_set))
        #print in_coup_not_gap_list,  in_gap_not_coup_list
        #gap_data = np.transpose(np.array(xyz_list_gap)-np.array(zero_point))
        #coup_data = np.transpose(np.array(xyz_list_coup)-np.array(zero_point))
        gap_data = np.transpose(np.array(xyz_list_gap)) #raw positions
        coup_data = np.transpose(np.array(xyz_list_coup))
        sink.send([in_coup_not_gap_set,in_gap_not_coup_set,gap_data,coup_data])

@coroutine
def sink():
    in_coup_not_gap_list=[]
    in_gap_not_coup_list=[]
    time = 0.0
    coup_unique_file = open('./coup_unique.out','w')
    gap_unique_file = open('./gap_unique.out','w')
    while True:
    	[coup_unique,gap_unique,gap_data,coup_data] = (yield)
        in_coup_not_gap_list.append(list(coup_unique))
        in_gap_not_coup_list.append(list(gap_unique))
        #print coup_unique 
	#print gap_unique
	#map(str,coup_unique)
	#map(str,gap_unique)
	#coup_unique_file.write(', '.join(coup_unique)+"\n"+str(time)+"\n")
	#gap_unique_file.write(', '.join(gap_unique)+"\n"+str(time)+"\n")
	coup_unique_file.write(' '.join(str(x) for x in coup_unique)+"\n"+str(time)+"\n")
	gap_unique_file.write(' '.join(str(x) for x in gap_unique)+"\n"+str(time)+"\n")
        #plt.scatter(coup_data[0],coup_data[1],color=next(colors))
        ax1.scatter(coup_data[0],coup_data[1])
	ax2.scatter(gap_data[0],gap_data[1])
        plt.savefig('./gap_coup_rank.png')
	time = time+0.1
	#plt.draw()
	
	#update.send(coup_data)	
	#plt.clf()
	#print gap_data
	#print coup_data
	#print "finish one loop"

@coroutine
def animate():
    while True:	
          data = (yield)
          scat._offsets3d = juggle_axes( data[0] , data[1] , data[2],'z' )
          #ax.view_init(30,0)

if __name__ == '__main__':
    # a1 = AnimatedScatter()
    # data_stream(filter(sink(animate())))
    # a1.show()
    # gap,coup = next(data_preprocess())
    # fig = plt.figure()
    # ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    # FLOOR = -15
    # CEILING = 15
    # ax.set_xlim3d(FLOOR,CEILING)
    # ax.set_ylim3d(FLOOR,CEILING)
    # ax.set_zlim3d(FLOOR,CEILING)
    # scat = ax.scatter([],[],[],animated=True)
    data_stream(filter(sink()))
    # instantiate the animator.
    # anim = animation.FuncAnimation(fig, animate,interval=30, blit=True)
    # fig.show()
    # print gap,coup
