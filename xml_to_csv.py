
"""
Go to the csv folder
 Operation mode: command line python xml2csv.py -i indir (picture and marked parent directory)
             Note: Required parameters: -i specifies the parent folder that contains pictures and annotations. Pictures and annotations may not be in the same subdirectory, but the names must correspond to each other
                                           (The picture format defaults to .jpg, if it is another format, you can modify the comments in the code yourself)
                     Optional parameters: -p split ratio of cross-validation set, default 0.05
                                       -t Generate training set CSV file name, default train.csv
                                       -v Generate cross-validation set CSV file name, default val.csv
                                       -c Generate class mapping CSV file name, default class.csv
"""
 
import os
import xml.etree.ElementTree as ET
import random
import math
import argparse
 
 
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--indir', type=str)
    parser.add_argument('-p', '--percent', type=float, default=0.1) #0.05
    parser.add_argument('-t', '--train', type=str, default='train.csv')
    parser.add_argument('-v', '--val', type=str, default='val.csv')
    parser.add_argument('-c', '--classes', type=str, default='class.csv')
    args = parser.parse_args()
    return args
 
 #Get a list of files with a specific suffix
def get_file_index(indir, postfix):
    file_list = []
    for root, dirs, files in os.walk(indir):
        for name in files:
            if postfix in name:
                file_list.append(os.path.join(root, name))
    return file_list
 
 #Write annotation information
def convert_annotation(csv, address_list):
    cls_list = []
    with open(csv, 'w') as f:
        for i, address in enumerate(address_list):
            in_file = open(address, encoding='utf8')
            strXml =in_file.read()
            in_file.close()
            root=ET.XML(strXml)
            for obj in root.iter('object'):
                cls = obj.find('name').text
                cls_list.append(cls)
                xmlbox = obj.find('bndbox')
                b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), 
                     int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
                f.write(file_dict[address_list[i]])
                f.write( "," + ",".join([str(a) for a in b]) + ',' + cls)
                f.write('\n')
    return cls_list
 
 
if __name__ == "__main__":
    args = parse_args()
    file_address = args.indir
    test_percent = args.percent
    train_csv = args.train
    test_csv = args.val
    class_csv = args.classes
    Annotations = get_file_index(file_address, '.xml')
    Annotations.sort()
         JPEGfiles = get_file_index(file_address,'.JPG') #Can be modified according to the suffix name of the image of your own data set
    JPEGfiles.sort()
         assert len(Annotations) == len(JPEGfiles) #If the XML file and the image file name cannot correspond to each other, an error will be reported
    file_dict = dict(zip(Annotations, JPEGfiles))
    num = len(Annotations)
    test = random.sample(k=math.ceil(num*test_percent), population=Annotations)
    train = list(set(Annotations) - set(test))
 
    cls_list1 = convert_annotation(train_csv, train)
    cls_list2 = convert_annotation(test_csv, test)
    cls_unique = list(set(cls_list1+cls_list2))
 
    with open(class_csv, 'w') as f:
        for i, cls in enumerate(cls_unique):
            f.write(cls + ',' + str(i) + '\n')
