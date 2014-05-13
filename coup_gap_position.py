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
import matplotlib.cm as cm
from relative_x_y import *
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

def data_stream_plot(target):
	with open(r'./coup_xy_relative_with_value.out') as coup:
		with open(r'./gap_xy_relative_with_value') as gap:
			for (b1,b2) in izip(read_in_chunk(coup),read_in_chunk(gap)):
				target.send([b1,b2])

distance_x_y = lambda x : (((x[0]-x[1])**2).sum())**0.5

@coroutine
def plot_coup_gap():
	"""@todo: Docstring for plot_coup_gap.

	:plot_data: @todo
	:returns: @todo

	"""
	time = 0
	while True:
		[coup,gap] = (yield)
		coup_array = np.asarray([x.split() for x in coup])
		gap_array = np.asarray([x.split() for x in gap])
#		plt.xlim((-10,60))
#		plt.ylim((-10,60))
		ax1 = plt.subplot(121)
		ax1.scatter(coup_array[:,0],coup_array[:,1])
		ax1.set_title('coup data')
		ax1.set_xlim([-10,60])
		ax1.set_ylim([-10,60])
		ax2 = plt.subplot(122)
		ax2.scatter(gap_array[:,0],gap_array[:,1])
		ax2.set_title('gap_data')
		ax2.set_xlim([-10,60])
		ax2.set_ylim([-10,60])
		plt.suptitle('Frame'+str(time))
		plt.savefig('timestep'+str(time)+'.png')
		time = time + 1
		plt.clf()
    



@coroutine
def filter(sink):
    #print "start receive"
    while True:
        [b1,b2,b3] = (yield)
        # print b1,b2,b3
	t,coup_rank,coup_value = zip(*[x.split() for x in b1])
        t,gap_rank,gap_value = zip(*[x.split() for x in b2])
        xyz_list = [x.split() for x in b3]
# remove first two text header
        xyz_list.pop(0) 
        del xyz_list[0]
#remove the first column of atom types such as Ar etc
        map(methodcaller("pop",0),xyz_list)
#convert string to float type
        xyz_list = [map(float,xyz) for xyz in xyz_list]
#point1 and point2 are positions of diatoms
	point1 = xyz_list[0]
	point2 = xyz_list[1]
	zero_point = [(x+y)/2 for (x,y) in zip(point1,point2)] 
        coup_rank = map(int,coup_rank)
        gap_rank = map(int,gap_rank)
        xyz_list_gap = [xyz_list[x] for x in gap_rank]
        xyz_list_coup = [xyz_list[x] for x in coup_rank]
#relative xy positions of Ar atom to diatoms in the same plane	
	xy_relative_gap = [relative_position_within_three_point(x, point1, point2) for x in xyz_list_gap]
	xy_relative_gap_with_value = merge_two_tuple(zip(xy_relative_gap,gap_value))
	xy_relative_coup = [relative_position_within_three_point(x, point1, point2) for x in xyz_list_coup]
	xy_relative_coup_with_value = merge_two_tuple(zip(xy_relative_coup,coup_value))
	sink.send([xy_relative_coup_with_value,xy_relative_gap_with_value])

@coroutine
def sink():
    coup_xy_relative_with_value_file = open('./coup_xy_relative_with_value.out', 'w')
    gap_xy_relative_with_value_file = open('./gap_xy_relative_with_value', 'w')
    while True:
	[coup_xy_relative_with_value, gap_xy_relative_with_value] = (yield)
	for t in coup_xy_relative_with_value:
		coup_xy_relative_with_value_file.write(' '.join(str(x) for x in t)+'\n')
	for t in gap_xy_relative_with_value:
		gap_xy_relative_with_value_file.write(' '.join(str(x) for x in t)+'\n')

@coroutine
def animate():
    while True:	
          data = (yield)
          scat._offsets3d = juggle_axes( data[0] , data[1] , data[2],'z' )
          #ax.view_init(30,0)
def merge_two_tuple(list_of_tuples):
	"""@todo: Docstring for merge_two_tuple within a list of tuple.

	:list_of_tuples: @todo
	:returns: @todo

	"""
        return [tuple(j for i in x for j in (i if isinstance(i,tuple) else (i,))) for x in list_of_tuples] 
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
    data_stream_plot(plot_coup_gap())
    # instantiate the animator.
    # anim = animation.FuncAnimation(fig, animate,interval=30, blit=True)
    # fig.show()
    # print gap,coup
