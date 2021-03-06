#!/usr/bin/env python
#-*- coding=utf-8 -*-
#########################################################
#Author:    Zhanshuai Meng
#Email: nju.mzs@outlook.com
#Created:   1 Dec 2015
########################################################
import math
import random
from collections import defaultdict
from collections import Counter

class Id3(object):
    def __init__(self, examples, labels, flags):
        self.examples = examples
        self.labels = labels
        self.flags = flags
        self.cut_value = {}
    def get_alter_point(self, examples,attr):
        """
        get attrs to use for numeric attribute
        """
        result = defaultdict(float)
        for example in examples:
            result[example] = self.examples[example][attr]
        sort_attr_values  = sorted(result.items(),key=lambda d:d[1])
        rtn = []
        for k in range(len(sort_attr_values)-1):
            example, value = sort_attr_values[k]
            example_pos,value_pos = sort_attr_values[k+1]
            if not (self.labels[example] ==self.labels[example_pos]):
                rtn.append(1.0/2*(value+value_pos))
        rtn = list(set(rtn))
        return rtn
    def cal_entropy(self, examples):
        """
        examples save indexes of the self.examples
        """
        class_freq = defaultdict(float)
        for example_index in examples:
            class_freq[self.labels[example_index]] += 1.0
        example_num = len(examples)
        entropy_vlaue = 0.0
        for freq_value in class_freq.values():
            entropy_vlaue += (-freq_value/example_num)* math.log(freq_value/example_num,2)
        return entropy_vlaue
    def get_best_attr_cut(self,examples,attr):
        """
        for numeric value
        return cut value of attr
        """
        alter_values = self.get_alter_point(examples,attr)
        all_values = self.get_attr_value(attr,examples)
        rtn_value = None
        entroy_base = 100.0
        for value in alter_values:
            example_less = [index for index in examples if self.examples[index][attr]<=value]
            example_greater = [index for index in examples if self.examples[index][attr]>value]
            total_sum = len(example_less)+len(example_greater)
            entroy_value = len(example_less)*1.0/total_sum*self.cal_entropy(example_less)+len(example_greater)*1.0/total_sum*self.cal_entropy(example_greater)
            if entroy_base >= entroy_value:
                entroy_base = entroy_value
                rtn_value = value
        return value

    def get_numeric_entroy(self,examples,attr):
        value = self.get_best_attr_cut(examples,attr)
        example_less = [index for index in examples if self.examples[index][attr]<=value]
        example_greater = [index for index in examples if self.examples[index][attr]>value]
        total_sum = len(example_less)+len(example_greater)
        entroy_value = len(example_less)*1.0/total_sum*self.cal_entropy(example_less)+len(example_greater)*1.0/total_sum*self.cal_entropy(example_greater)
        return entroy_value



    def cal_gain(self, examples, attr):
        """
        attr is the index of the selected feature
        examples is the index of the self.examples
        """
        if self.flags[attr] == 0:
            return self.cal_entropy(examples) - self.get_numeric_entroy(examples,attr)
        attr_freq = defaultdict(float)
        for row_index in examples:
            example = self.examples[row_index]
            attr_freq[example[attr]] += 1.0
        examples_sum = sum(attr_freq.values())
        sum_subentropy = 0.0
        for attr_key in attr_freq.keys():
            attr_perc = attr_freq[attr_key]/examples_sum
            sub_examples = [example for example in examples if self.examples[example][attr] == attr_key]
            sum_subentropy += attr_perc*self.cal_entropy(sub_examples)
        return self.cal_entropy(examples) - sum_subentropy

    def get_best_attr(self,examples,attrs):
        """
        choose the best attribute based on gain or entropy
        attrs is the list of index of the alternative attributes
        """
        chosen_attr = None
        best_fit = 0.0
        for attr in attrs:
            fitness_value = self.cal_gain(examples,attr)
            if fitness_value>best_fit:
                best_fit =  fitness_value
                chosen_attr = attr
        return chosen_attr
    def get_match_examples(self,attr,attr_value,examples=None):
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
        if not examples:
          examples=range(len(self.examples))
        rtn_examples = [index for index in examples if self.examples[index][attr] == attr_value]
        return rtn_examples

    def get_attr_value(self, attr,examples=None):
        """
        examples is the list of index
        attr is the index of chosen attribute
        return unique values of the given attribute
        """
        if not examples:
          examples=range(len(self.examples))
        examples_data = [self.examples[index][attr] for index in examples]
        examples_data = list(set(examples_data))
        return examples_data

    def default_class(self,examples=None):
        if not examples:
          examples=range(len(self.examples))
        label_data = [self.labels[index] for index in examples]
        counter = dict(Counter(label_data))
        sort_counter  = sorted(counter.items(),key=lambda d:d[1],reverse=1)
        return sort_counter[0][0]


    def decision_tree(self,examples,attributes,q=None):
        """
        examplexs save the index list of the records
        attributes is the list of index of alternative attributes for records
        attribute_genfunc function is for random forests alg
        """
        examples = examples[:]
        default_class = self.default_class(examples)
        labels = [self.labels[index] for index in examples]
        if len(attributes) <= 1 or not examples:
            return default_class
        elif labels.count(labels[0]) == len(labels):
        	return labels[0]
        else:
            if q:
                alter_attributes = self.attributes_gen(q,attributes)
            else:
                alter_attributes = attributes[:]
            chosen_attr = self.get_best_attr(examples,alter_attributes)
            if not chosen_attr:
                chosen_attr = attributes[0]
            node = {chosen_attr:{}}
            #if not q:
            if attributes.count(chosen_attr)>0:
                attributes.remove(chosen_attr)
            if self.flags[chosen_attr] == 0:
                attr_cut_value = self.get_best_attr_cut(examples,chosen_attr)
                self.cut_value[chosen_attr] = attr_cut_value
                examples_less = [index for index in examples if self.examples[index][chosen_attr]<=attr_cut_value]
                examples_greater = [index for index in examples if self.examples[index][chosen_attr]>attr_cut_value]
                if examples_less and examples_greater:
                	less_tree_node = self.decision_tree(examples_less,attributes,q)
                	greater_tree_node = self.decision_tree(examples_greater,attributes,q)
                	node[chosen_attr][-1] = less_tree_node
                	node[chosen_attr][1] = greater_tree_node
            	else:
            		examples_less += examples_greater
            		less_tree_node = self.decision_tree(examples_less,attributes,q)
            		node[chosen_attr][-1] = less_tree_node
           		node[chosen_attr][1] = less_tree_node
            else:
                for value in self.get_attr_value(chosen_attr,examples):
                    match_examples = self.get_match_examples(chosen_attr,value,examples)
                    sub_tree_node = self.decision_tree(match_examples,attributes,q)
                    node[chosen_attr][value] = sub_tree_node
        return node

    def get_label_count(self,tree):
        if not type(tree) == dict:
            label_count = defaultdict(float)
            label_count[tree] += 1.0
            return label_count
        attr, branches = tree.items()[0]
        counts = defaultdict(float)
        for branch in branches.values():
            results = self.get_label_count(branch)
            for key in [-1.0,1.0]:
                counts[key] += results[key]
        return counts

    def get_majority_label(self,tree):
        count = self.get_label_count(tree)
        label = None
        counter = 0.0
        for key in count.keys():
            if count[key] >= counter:
                counter = count[key]
                label = key
        return label

    def attributes_gen(self,q,attributes):
        """
        q is the number of selected attributes by random forests
        """
        rtn_attributes = []
        if len(attributes) <= q:
        	rtn_attributes = attributes[:]
        	return rtn_attributes
        for i in range(int(q)):
            attr = None
            while (attr in rtn_attributes or not (attr)):
                attr = random.randint(0,len(self.examples[0])-1)
            rtn_attributes.append(attr)
        return rtn_attributes

    def get_classification(self,record,tree):
        """
        Return the class label of the given record
        """
        if not type(tree) == dict:
            return tree
        else:
            attr,branch = tree.items()[0]
            if self.flags[attr] == 1:
                if not branch.has_key(record[attr]):
                    return self.get_majority_label(tree)
                sub_tree = branch[record[attr]]
                return self.get_classification(record,sub_tree)
            else:
                attr_value = record[attr]
                cut_attr_value = self.cut_value[attr]
                if attr_value < cut_attr_value:
                    return self.get_classification(record,branch[-1])
                else:
                    return self.get_classification(record,branch[1])

    def get_class_labels(self,test_set,tree):
        """
        test_set is the data set of instances to be classified
        """
        data = test_set[:]
        results = []
        for record in data:
            label = self.get_classification(record,tree)
            results.append(label)
        return results
    def conduct(self,test_set,test_label):
        """
        test_set is the list of instances
        return error_rate and result of labels
        """
        tree = self.decision_tree(range(len(self.examples)),range(len(self.examples[0])))
        result = self.get_class_labels(test_set,tree)
        com_result = [result[i]==test_label[i] for i in range(len(result))]
        accurate_rate = com_result.count(True)*1.0/len(test_label)
        return accurate_rate, result







