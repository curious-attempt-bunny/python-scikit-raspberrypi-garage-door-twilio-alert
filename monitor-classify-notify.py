#!/usr/bin/env python

import os
import time
from glob import glob
from sklearn.linear_model import LogisticRegression
import json
import numpy as np
from PIL import Image

monitor_directory = os.environ['MONITOR_DIRECTORY'] if os.environ.has_key('MONITOR_DIRECTORY') else '/var/lib/motion'
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

existing = set()

while poll:
    filenames = set(glob(monitor_directory+'/*.jpg'))

    candidates = filenames.difference(existing)

    for candidate in candidates:
        print 'New image:', candidate

        x = np.reshape(np.asarray(Image.open(candidate).convert('L')), (-1))
        y = clf.predict([x])[0]

        print y
        existing.add(candidate)

    time.sleep(0.2)