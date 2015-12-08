#!/usr/bin/env python
#-*- coding=utf-8 -*-
#from Adaboost import Ada
#from Forests import RandomForests
#from ID3 import Id3
#from ID3 import Id3
import ID3
import Adaboost
import Forests
import sys

alg={1:ID3.Id3,2:Forests.RandomForests,3:Adaboost.Ada}
data={1:'./data1.txt',2:'./data2.txt'}
def get_data(datafile):
    data = []
    label = []
    with open(datafile,'r') as f:
        line_first = f.readline()  #Skip the first line
        item_l = line_first.split(',')
        flags = [int(value.strip()) for index, value in enumerate(item_l) if index < len(item_l)]
        for line in f:
            item_list = line.split(',')
            features = [float(value.strip()) for index, value in enumerate(item_list) if index < (len(item_list)-1)]
            tag = float(item_list[len(item_list)-1].strip())
            if tag<=0.0:
            	tag = -1.0
            data.append(features)
            label.append(tag)
    return data, label, flags

def get_k_fold(examples, labels, k=10):
    """
    examples and labels are both the list of instances here
    """
    example_fold = []
    label_fold = []
    interval = int(len(examples)/k)
    for i in range(k):
    	#f_examples = [examples[j] for j in range(len(examples)) if j%k == i]
        #f_labels = [labels[j] for j in range(len(labels)) if j%k == i]
        f_examples = [examples[j] for j in range(interval*i,interval*(i+1))]
        f_labels = [labels[j] for j in range(interval*i,interval*(i+1))]
        example_fold.append(f_examples)
        label_fold.append(f_labels)
    return example_fold, label_fold

def k_fold_validation(alg,example_fold,label_fold,flags):
    """
    alg: Id3, Ada, RandomForests
    example_fold and label_fold are both the list of instances
    Return the mean and standard deviation accuracy
    """
    k = len(example_fold)
    accu_rate = []
    print "-------------",alg,"---------------"
    for i in range(k):
        print "******** ",i,"-fold *******"
        training_set = []
        training_label = []
        testing_set = example_fold[i]
        testing_label = label_fold[i]
        for j in range(k):
            if not j == i:
                training_set += example_fold[j]
                training_label += label_fold[j]
        alg_run = alg(training_set, training_label,flags)
        accurate_rate, result = alg_run.conduct(testing_set,testing_label)
        print "accurate rate: ",accurate_rate
        accu_rate.append(accurate_rate)
    mean_accu = mean(accu_rate)
    stdev_accu = pstdev(accu_rate)
    return mean_accu,stdev_accu

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

if __name__ == '__main__':
    if (not (len(sys.argv) == 3)) or not (int(sys.argv[1]) in range(1,4)) or not (int(sys.argv[2]) in range(1,3)):
        print '     Usage: python filename (1,2,3) (1,2)'
        print '            (1,2,3) for ID3.Id3, Forests.RandomForests, Adaboost.Ada'
        print '            (1,2) for data1, data2'
        exit()
    data,label,flags = get_data(data[int(sys.argv[2])])
    example_fold, label_fold = get_k_fold(data,label,10)
    # ID3.Id3, Adaboost.Ada,Forests.RandomForests
    mean_accu, stdev_accu = k_fold_validation(alg[int(sys.argv[1])],example_fold,label_fold,flags)
    print mean_accu,stdev_accu




