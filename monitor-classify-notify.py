#!/usr/bin/env python

import os
import time
from glob import glob
from sklearn.linear_model import LogisticRegression
import json
import numpy as np
from PIL import Image

monitor_directory = os.environ['MONITOR_DIRECTORY'] if os.environ.has_key('MONITOR_DIRECTORY') else '/var/lib/motion'
label_directory = os.environ['LABEL_DIRECTORY'] if os.environ.has_key('LABEL_DIRECTORY') else monitor_directory+'/label'
poll = os.environ['POLL'] == 'true' if os.environ.has_key('POLL') else False

print 'Monitor directory:', monitor_directory
print 'Poll:', poll

with open('classifier.json') as data_file:    
    clf_dict = json.load(data_file)
clf = LogisticRegression()
clf.set_params(**clf_dict['params'])
clf.coef_ = np.asarray(clf_dict['coef_'])
clf.intercept_ = np.asarray(clf_dict['intercept_'])
clf.n_iter_ = np.asarray(clf_dict['n_iter_'])
clf.classes_ = np.asarray(clf_dict['classes_'])

labelled = set()
while True:
    candidates = set(glob(monitor_directory+'/*.jpg'))
    
    for candidate in candidates:
        name = candidate.split('/')[-1]
        print name

        if name in labelled:
            continue
        if os.path.isfile(label_directory+'/error/'+name) or os.path.isfile(label_directory+'/guess/open/'+name) or os.path.isfile(label_directory+'/guess/closed/'+name) or os.path.isfile(label_directory+'/known/open/'+name) or os.path.isfile(label_directory+'/known/closed/'+name):
            labelled.add(name)
            continue

        print 'New image:', candidate

        try:
            x = np.reshape(np.asarray(Image.open(candidate).convert('L')), (-1))
            y = clf.predict([x])[0]

            # print y

            if y == 1:
                label = 'open'
            else:
                label = 'closed'
            directory = label_directory+'/guess/'+label+'/'

        except IOError:
            label = 'error'
            directory = label_directory+'/error/'

        target = candidate.replace(monitor_directory+'/', directory)

        print '--->', target

        os.link(candidate, target)

    if not poll:
        break

    time.sleep(0.2)