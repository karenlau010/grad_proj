import os
from svmutil import *

def train_default():
    y, x = svm_read_problem('./input_data/heart_scale')
    m = svm_train(y[:200], x[:200], '-c 4')
    p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)

def train_drive(train_file, test_file):
    y_tr, x_tr = svm_read_problem(os.path.join('./input_data', train_file))
    m = svm_train(y_tr, x_tr, '-c 4')
    y_ts, x_ts = svm_read_problem(os.path.join('./input_data', test_file))
    p_label, p_acc, p_val = svm_predict(y_ts, x_ts, m)

def tran2vect():
    pass

if __name__ == "__main__":
    ###train_default()
    train_drive('train_data', 'test_data')
