#!/usr/bin/env python -u


#import sys, json, math
from spam_detector_commons import *

def compute_precision_recall(curr_class, actual, computed):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i in range(0, len(actual)):
        if actual[i] == curr_class:
            if computed[i] == curr_class:
                tp +=1
            else:
                fn += 1
        else:
            if computed[i] == curr_class:
                fp += 1
            else:
                tn += 1
    
    if(tp==0 and fp == 0):
        precision = -1
    else:
        precision = float(tp)/(tp + fp)
    if(tp == 0 and fn == 0):
        recall = -1
    else:
       recall = float(tp)/(tp + fn)
    return [precision, recall]

def spam_classifer(text):
    
    model = readModel('spam_filter_model.txt')
    marker =  classify(model, text)
    print marker
    compute_precision_recall()
    
    return marker
    