import numpy as np
import pypcd
import datetime
import os
import math
from struct import Struct


def write_records(records, format, f):
    """
    Write a sequence of tuples to a binary file of structures.
    """
    record_struct = Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))

'''
def pointAssociateToMap(pi, transformTobeMapped):
    x1 = math.cos(transformTobeMapped[2]) * pi[0] - math.sin(transformTobeMapped[2]) * pi[1]
    y1 = math.sin(transformTobeMapped[2]) * pi[0] + math.cos(transformTobeMapped[2]) * pi[1]
    z1 = pi[2]

    x2 = x1
    y2 = math.cos(transformTobeMapped[0]) * y1 - math.sin(transformTobeMapped[0]) * z1
    z2 = math.sin(transformTobeMapped[0]) * y1 + math.cos(transformTobeMapped[0]) * z1

    t1 = math.cos(transformTobeMapped[1]) * x2 + math.sin(transformTobeMapped[1]) * z2 + transformTobeMapped[3]
    t2 = y2 + transformTobeMapped[4]
    t3 = -math.sin(transformTobeMapped[1]) * x2 + math.cos(transformTobeMapped[1]) * z2 + transformTobeMapped[5]
    t4 = pi[3]
    tmp = [t1, t2, t3, t4]
    return tmp
'''


# load_global_map(f, db, drop) reads pcd data in f (*.pcd) into Mongodb collection db.offlinemap
# The format is as {"loc": [x, z], "y": [y]}
# By default, when drop==False, it would append new data without remove old points.
# To remove old data in db.offline, please set drop=True
def load_global_map(filelist):
    start = datetime.datetime.now()
    point_to_block = {}
    block_size = 20
    count = 0
    for f in filelist:
        count += 1
        print count
        # print "Reading pcd...\n" + f + "\n"
        pc = pypcd.PointCloud.from_path(f)
        global_map = pc.pc_data
        # print datetime.datetime.now() - start

        '''
        txtfile = os.path.join(FindPath, f[:-4] + ".txt")
        mat_list = []
        with open(txtfile) as infile:
            for line in infile:
                fields = line.split()
                mat_list.extend(map(float, fields))
        '''
        # print "Dumping...\n"
        for point in global_map:
            '''
            sin2 = math.sin(mat_list[2])
            cos2 = math.cos(mat_list[2])
            sin1 = math.sin(mat_list[1])
            cos1 = math.cos(mat_list[1])
            sin0 = math.sin(mat_list[0])
            cos0 = math.cos(mat_list[0])
            x1 = cos2 * point[0] - sin2 * point[1]
            y1 = sin2 * point[0] + cos2 * point[1]
            z1 = point[2]

            x2 = x1
            y2 = cos0 * y1 - sin0 * z1
            z2 = sin0 * y1 + cos0 * z1

            t0 = cos1 * x2 + sin1 * z2 + mat_list[3]
            t1 = y2 + mat_list[4]
            t2 = -sin1 * x2 + math.cos(mat_list[1]) * z2 + mat_list[5]
            t3 = point[3]
            '''
            x_block = int(np.round(point[0]/block_size))*block_size
            z_block = int(np.round(point[2]/block_size))*block_size
            block_tuple = (x_block, z_block)
            point_to_block.setdefault(block_tuple, []).append((point[0], point[2], point[1], point[3]))
            # point_to_block: block->(x,z,y)

    print "Writing...\n"
    destination_folder = "/mnt/truenas/scratch/genmao/one_map_files/"
    block_start = 0
    block_index = []
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    blockfilename = destination_folder + "map1492801000.06.txt"
    with open(blockfilename, 'ab') as outfile:
        for cell in point_to_block:
            # flatten = [item for sublist in point_to_block[cell] for item in sublist]
            print block_start
            block_index.append((cell[0], cell[1], block_start, block_start + len(point_to_block[cell])))
            block_start += len(point_to_block[cell])
            write_records(point_to_block[cell], '<dddd', outfile)
    block_indexfile = destination_folder + "idx1492801000.06.txt"
    with open(block_indexfile, 'wb') as outfile:
        write_records(block_index, '<dddd', outfile)
    print datetime.datetime.now() - start


if __name__ == "__main__":
    FindPath = "/mnt/truenas/scratch/yiluo/ToGenmao/1492801000.06/mappoints"
    FileList = []
    FileNames = os.listdir(FindPath)
    if len(FileNames) > 0:
        for f in FileNames:
            if os.path.splitext(f)[-1] == ".pcd":
                pcdfile = os.path.join(FindPath, f)
                FileList.append(pcdfile)
    load_global_map(FileList)
    # pcdfile = '/home/genmaoshi/Downloads/data_sample/1486176044.29.pcd'
    # pcdfile = '/home/genmaoshi/Downloads/data_sample/part.pcd'

