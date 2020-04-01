#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' This is a demo file for the Invariants Mining model.
    API usage:
        dataloader.load_HDFS(): load HDFS dataset
        feature_extractor.fit_transform(): fit and transform features
        feature_extractor.transform(): feature transform after fitting
        model.fit(): fit the model
        model.predict(): predict anomalies on given data
        model.evaluate(): evaluate model accuracy with labeled data
'''

import sys
sys.path.append('../')
from loglizer.models import InvariantsMiner
from loglizer import dataloader, preprocessing

#struct_log = '../data/HDFS/HDFS_100k.log_structured.csv' # The structured log file
struct_log = '../data/HDFS/syslog_200000.log_structed.csv'
epsilon = 0.5 # threshold for estimating invariant space

if __name__ == '__main__':
    # Load structured log without label info
    (x_train, _), (x_test, _), data_df = dataloader.load_HDFS(struct_log,
                                                     window='session', 
                                                     train_ratio=0.5,
                                                     split_type='sequential')

    # Feature extraction
    feature_extractor = preprocessing.FeatureExtractor()
    x_train = feature_extractor.fit_transform(x_train)

    # Model initialization and training
    model = InvariantsMiner(epsilon=epsilon)
    model.fit(x_train)

    # Predict anomalies on the training set offline, and manually check for correctness
    y_train = model.predict(x_train)

    # Predict anomalies on the test set to simulate the online mode
    # x_test may be loaded from another log file
    x_test = feature_extractor.transform(x_test)
    y_test = model.predict(x_test)

    # Summarize anomalies
    anomalies = []
    anomalies_val = []
    for i in range(len(y_train)):
        if y_train[i] != 0:
            anomalies.append(i)

    for i in range(len(y_test)):
        if y_test[i] != 0:
            anomalies.append(i + len(y_train))

    print("Total number of log entries: {} | Total number of anomalies: {}".format(
            10* (len(y_train) + len(y_test)),
            len(anomalies)
            )
        )
    print("Index of blocks that contains anomaly: \n{}".format(anomalies))

