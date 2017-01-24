#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015

This script is to convert the txt annotation files to appropriate format needed by YOLO 

@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

"""
Modified by Adam Allevato, 1/24/2017
http://allevato.me
"""

import os
from os import walk, getcwd
from PIL import Image
import sys
import shutil

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def main():
    if len(sys.argv) < 2:
        print 'please provide all classes as command-line arguments'
        return
    classes = sys.argv[1:]

    wd = getcwd()

    output_dir = wd + "/Output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    annotations_dir = wd + "/Output/annotations"
    if not os.path.exists(annotations_dir):
        os.mkdir(annotations_dir)
    images_dir = wd + "/Output/images"
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    list_file = open(output_dir + '/list.txt', 'w')
    for this_class in classes:
        """ Configure Paths"""   

        class_labels_dir = wd + "/Labels/" + this_class + "/"
        output_annotations_dir = wd + "/Output/annotations/" + this_class + "/"
        if not os.path.exists(output_annotations_dir):
            os.mkdir(output_annotations_dir)
        output_images_dir = wd + "/Output/images/" + this_class + "/"
        if not os.path.exists(output_images_dir):
            os.mkdir(output_images_dir)

        cls_id = classes.index(this_class)
        print "class id: " + str(cls_id)


        """ Get input text file list """
        txt_name_list = []
        for (dirpath, dirnames, filenames) in walk(class_labels_dir):
            txt_name_list.extend(filenames)
            break
        print(txt_name_list)

        """ Process """
        for txt_name in txt_name_list:
            # txt_file =  open("Labels/stop_sign/001.txt", "r")
            
            """ Open input text files """
            txt_path = class_labels_dir + txt_name
            print("Input:" + txt_path)
            txt_file = open(txt_path, "r")
            lines = txt_file.read().split('\n')
            
            """ Open output text files """
            txt_output_annotations_dir = output_annotations_dir + txt_name
            print("Output:" + txt_output_annotations_dir)
            txt_outfile = open(txt_output_annotations_dir, "w")
            
            
            """ Convert the data to YOLO format """
            ct = 0
            infile_path = str('%s/Images/%s/%s.jpg'%(wd, this_class, os.path.splitext(txt_name)[0]))
            im=Image.open(infile_path)
            for (idx, line) in enumerate(lines):
                if(idx > 1 and len(line) > 4):
                    print('processing line ' + line)
                    ct = ct + 1
                    print(line)
                    elems = line.split(' ')
                    print("elems: " + str(elems))
                    xmin = elems[0]
                    xmax = elems[2]
                    ymin = elems[1]
                    ymax = elems[3]
                    #
                    #t = magic.from_file(img_path)
                    #wh= re.search('(\d+) x (\d+)', t).groups()
                    w= int(im.size[0])
                    h= int(im.size[1])
                    #w = int(xmax) - int(xmin)
                    #h = int(ymax) - int(ymin)
                    # print(xmin)
                    print(w, h)
                    b = (float(xmin), float(xmax), float(ymin), float(ymax))
                    bb = convert((w,h), b)
                    print(bb)
                    print(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                    txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            txt_outfile.flush()
            txt_outfile.close()

            """ Save those images with bb into list"""
            if(ct != 0):
                list_path = output_images_dir + '%s.jpg'%(os.path.splitext(txt_name)[0])
                list_file.write(list_path + '\n')

                shutil.copy(infile_path, output_images_dir)
                        
    list_file.close()

if __name__ == '__main__':
    main()