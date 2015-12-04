#!/usr/bin/env python
#-*- coding=utf-8 -*-
#########################################################
#Author:    Zhanshuai Meng
#Email: nju.mzs@outlook.com
#Created:   1 Dec 2015
########################################################
import math
from collections import defaultdict
from collections import Counter

class Id3(object):
    def __init__(self, examples, labels):
        self.examples = examples
        self.labels = labels

    def cal_entropy(self, examples):
        """
        examples save indexes of the self.examples
        """
        class_freq = defaultdict(dict)
        for example_index in examples:
            class_freq[label[example_index]] += 1.0
        example_num = len(examples)
        entropy_vlaue = 0
        for freq_value in class_freq.values():
            entropy_vlaue += (-freq_value/example_num)* math.log(freq_value/example_num,2)
        return entropy_vlaue
    def cal_gain(self, examples, attr):
        """
        attr is the index of the selected feature
        examples is the index of the self.examples
        """
        attr_freq = defaultdict(dict)
        for row_index in examples:
            example = self.examples[row_index]
            attr_freq[example[attr]] += 1.0
        examples_sum = sum(attr_freq.values())
        sum_subentropy = 0.0
        for attr_key in attr_freq.keys():
            attr_perc = attr_freq[attr_key]/examples_sum
            sub_examples = [example for example in examples if self.examples[example][attr] == attr_key]
            sum_subentropy += self.cal_entropy(sub_examples)

        return entropy(data) - sum_subentropy
    def get_best_attr(self,examples,attrs):
        """
        choose the best attribute based on gain or entropy
        attrs is the list of index of the alternative attributes
        """
        chosen_attr = None
        best_fit = 0.0
        for attr in attrs:
            fitness_value = fit_func(examples,attr)
            if(fitness_value>best_fit):
                best_fit =  fitness_value
                chosen_attr = attr
        return best_attr
    def get_match_examples(self,attr,attr_value,examples=range(len(self.examples))):
        """
        examples saves the index list of examples
        attr is the index of attribute
        attr_value is the value to match
        """
        #example_pool = self.examples[:]
        #rtn_examples = []
        #for i in examples:
        #    if examples_pool[i][attr] == attr_value:
        #        rtn_examples.append(i)
        rtn_examples = []
        rtn_examples = [index for index,value in enumerate(self.examples) if value[attr] == attr_value]
        return rtn_examples

    def get_attr_value(self, attr,examples=range(len(self.examples))):
        """
        examples is the list of index
        attr is the index of chosen attribute
        return unique values of the given attribute
        """
        examples_data = [value for index,value in enumerate(self.examples) if index in examples]
        examples_data = list(set(examples_data))
        return examples_data

    def default_class(self,examples=range(len(self.examples))):
        label_data = [label for index, label in enumerate(self.labels) if index in examples]
        counter = dict(Counter(label_data))
        sort_counter  = sorted(counter.items(),key=lambda d:d[0])
        return sort_counter.values()[0]


    def decision_tree(self,examples,attributes):
        """
        examplexs save the index list of the records
        attributes is the list of index of alternative attributes for records
        """
        default_class = self.default_class(examples)
        labels = [self.labels[index] for index in examples]
        #if all the examples have the same label, return the label as the leaf node
        if labels.count(labels[0]) == len(labels):
            return labels[0]
        #No attribute is alternative
        elif len(attributes) < 1 and not examples:
            return default_class
        else:
            chosen_attr = self.get_best_attr(examples,attributes)
            node = {chosen_attr:{}}
            for value in self.get_attr_value(chosen_attr,examples):
                match_examples = self.get_match_examples(chosen,value,examples)
                sub_tree_node = self.decision_tree(match_examples,attributes.remove(chosen_attr))
                node[chosen_attr][value] = sub_tree_node
        return node

