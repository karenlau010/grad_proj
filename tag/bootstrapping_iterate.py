# -*- coding: utf-8 -*-

import pynlpir
import sys
import re
import os
import time

#decode: str ==> unicode
#encode: unicode ==> str
encode_type = sys.getfilesystemencoding() #UTF-8 in my machine

cur_rule_set = set()
raw_rule_set = set()

def init_rule():
    global raw_rule_set
    fp_rule_raw = file('./after_tag/rule_generalize.xxx', 'rb')
    for raw_rule in fp_rule_raw:
        raw_rule = (raw_rule.strip()).decode('UTF-8')
        raw_rule_set.add(raw_rule)
    fp_rule_raw.close()
    raw2re()

def raw2re():
    global cur_rule_set
    global raw_rule_set
    for raw_rule in raw_rule_set:
        pass

def match_rule():
    global cur_rule_set

def cop_file(in_path, out_path):
    fp_in = file(in_path, 'rb')
    fp_out = file(out_path, 'wb')
    for line in fp_in:
        fp_out.write(line)
    fp_in.close()
    fp_out.close()

def file_add(base_file, add_file):
    fp_base = file(base_file, 'ab')
    fp_add = file(add_file, 'rb')
    for add_line in fp_add:
        fp_base.write(add_line)
    fp_base.close()
    fp_add.close()

def single_iterate():
    cop_file('./after_tag/U.xxx', './after_tag/U.xxx_tmp')
    fp_U_in = file('./after_tag/U.xxx_tmp', 'rb')
    fp_U_out = file('./after_tag/U.xxx', 'wb')
    fp_U_prime = file('./after_tag/U_prime.xxx', 'wb')
    part_no = 4
    count = 0
    part_lines = []
    for u_sent in fp_U_in:
        part_lines.append(u_sent.strip())
        count += 1
        if count == 4:
            count = 0
            ###TODO...
            ###DONE...
            part_lines = []
    fp_U_in.close()
    os.remove('./after_tag/U.xxx_tmp')
    fp_U_out.close()
    fp_U_prime.close()
    file_add('./after_tag/L.xxx', './after_tag/U_prime.xxx') # L+U'->L

def drive_iterate():
    iterate_times = 1 #terminate by the iterate_times
    for iterate_i in range(iterate_times):
        single_iterate()

if __name__ == "__main__":
    init_rule()
    drive_iterate()
