#!/usr/bin/env python
#-*- coding=utf-8 -*-
#from Adaboost import Ada
#from Forests import RandomForests
#from ID3 import Id3
#from ID3 import Id3
import ID3
import Adaboost
import Forests

def get_data(datafile):
    data = []
    label = []
    with open(datafile,'r') as f:
        f.readline()  #Skip the first line
        for line in f:
            item_list = line.split(',')
            features = [float(value.strip()) for index, value in enumerate(item_list) if index < (len(item_list)-1)]
            tag = float(item_list[len(item_list)-1].strip())
            data.append(features)
            label.append(tag)
    return data, label

def get_k_fold(examples, labels, k=10):
    """
    examples and labels are both the list of instances here
    """
    example_fold = []
    label_fold = []
    print 'labels',len(labels)
    interval = int(len(examples)/k)
    print 'interval: ',interval
    for i in range(k):
        f_examples = [examples[j] for j in range(interval*i,interval*(i+1))]
        f_labels = [labels[k] for k in range(interval*i,interval*(i+1))]
        example_fold.append(f_examples)
        label_fold.append(f_labels)
    return example_fold, label_fold

def k_fold_validation(alg,example_fold,label_fold):
    """
    alg: Id3, Ada, RandomForests
    example_fold and label_fold are both the list of instances
    Return the mean and standard deviation accuracy
    """
    k = len(example_fold)
    print 'examples fold: ',k
    accu_rate = []
    for i in range(k):
        training_set = []
        training_label = []
        testing_set = example_fold[i]
        testing_label = label_fold[i]
        for j in range(k):
            if not j == i:
                training_set += example_fold[j]
                training_label += label_fold[j]
        print 'tring len ',len(training_set),' ',len(training_label)
        print 'testing len ',len(testing_set),' ',len(testing_label)
        alg_run = alg(training_set, training_label)
        accurate_rate, result = alg_run.conduct(testing_set,testing_label)
        print 'accurate ', accurate_rate
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
    data,label = get_data('./data1.txt')
    forests = Forests.RandomForests(data,label)
    accut, result = forests.conduct(data,label)
    print accut
    example_fold, label_fold = get_k_fold(data,label,10)
    mean_accu, stdev_accu = k_fold_validation(Forests.RandomForests,example_fold,label_fold)
    print mean_accu,stdev_accu



