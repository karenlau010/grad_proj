# -*- coding: utf-8 -*-

import pynlpir
import sys
import re
import os
import time
from bootstrapping_init import *

#decode: str ==> unicode
#encode: unicode ==> str
encode_type = sys.getfilesystemencoding() #UTF-8 in my machine

rep_dict = {u"\[\[<MED>\d+\]\]":u"<MED>", u"\[\[.{0,5}<DIS>.{0,5}\d+\]\]":u"<DIS>", \
                u"\[\[.{0,5}<SYM>.{0,5}\d+\]\]":u"<SYM>", u"\[\[<TRE>\d+\]\]":u"<TRE>"}

cur_rule_set = set()
raw_rule_set = set()
match_count = 0

def init_rule():
    global raw_rule_set
    fp_rule_raw = file('./after_tag/rule_generalize.xxx', 'rb')
    for raw_rule in fp_rule_raw:
        raw_rule = (raw_rule.strip()).decode('UTF-8')
        raw_rule_set.add(raw_rule)
    fp_rule_raw.close()
    raw2re()

def raw2re_extend_part(re_rule):
    re_rule = re_rule.split('|')
    assert re_rule[0] != u''
    for re_i in range(len(re_rule)):
        re_rule[re_i] = re.sub("^.*/", '', re_rule[re_i], count=1, flags=0) #only retain the tagging
    re_rule = ' '.join(re_rule)
    return re_rule

def extend2re(re_rule):
    re_rule = re_rule.split()
    if re_rule[0] == '*' or re_rule[0] == u'*': #remove the head
        re_rule = re_rule[1:]
    if re_rule[-1] == '*' or re_rule[-1] == u'*': #remove the tail
        re_rule = re_rule[:-1]
    re_rule = '|'.join(re_rule)
    ###for k,v in rep_dict.iteritems(): #Don't need to trans
    ###    re_rule = re_rule.replace(v, k)
    re_rule = re_rule.replace('*', '.*')
    re_rule = re_rule.replace('|.*', '.*')
    re_rule = re_rule.replace('.*|', '.*')
    return re_rule

def raw2re():
    global cur_rule_set
    global raw_rule_set
    global rep_dict
    fp_re = file('./after_tag/re_generalize.xxx', 'wb')
    for raw_rule in raw_rule_set:
        raw_rule = raw_rule.split()
        re_rule = raw_rule[0]
        re_lest = ' '.join(raw_rule[1:])
        fp_re.write('>>> '+re_rule.encode('UTF-8')+' '+re_lest.encode('UTF-8')+'\n')
        re_rule = raw2re_extend_part(re_rule)
        re_rule = extend2re(re_rule)
        fp_re.write(re_rule.encode('UTF-8')+' '+re_lest.encode('UTF-8')+'\n')
        cur_rule_set.add(re_rule+' '+re_lest)
    fp_re.close()

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

def pre_sent(raw_string, tag_string, ne_list):
    seg_line = deal_cws(raw_string)
    ne_pos_list = cal_ne_pos(tag_string, ne_list)
    seg_line = comb_ne_cws(seg_line, ne_pos_list)
    #seg_line = rm_stop_w(seg_line) #there should't remove the stop words
    seg_line = pos_cont_w(seg_line) #the function should be completed
    ret_sent = gen_rule(seg_line)
    ret_sent = raw2re_extend_part(ret_sent)
    return ret_sent

def match_rule(pre_sent):
    global cur_rule_set
    global match_count
    for rule_i in cur_rule_set:
        rule_i = rule_i.split()
        rule_part = rule_i[0]
        rule_type = rule_i[1]
        rule_flag = rule_i[2:]
        rule_part = rule_part.replace('|', ' ')
        find_ret = re.findall(rule_part, pre_sent)
        if len(find_ret) > 0:
            match_count += 1
            return True
    return False

def single_iterate():
    cop_file('./after_tag/U.xxx', './after_tag/U.xxx_tmp')
    fp_U_in = file('./after_tag/U.xxx_tmp', 'rb')
    fp_U_out = file('./after_tag/U.xxx', 'wb')
    fp_U_prime = file('./after_tag/U_prime.xxx', 'wb')
    fp_pre = file('./after_tag/pre.xxx', 'wb')
    part_no = 4
    count = 0
    part_lines = []
    for u_sent in fp_U_in:
        part_lines.append(u_sent.strip())
        count += 1
        if count == 4:
            count = 0
            ###TODO...
            raw_string = part_lines[1].decode('UTF-8')
            ner_string = part_lines[2].decode('UTF-8')
            ne_list = ((part_lines[3].decode('UTF-8')).split())[1:]
            pre_ret = pre_sent(raw_string, ner_string, ne_list)
            if match_rule(pre_ret) == True:
                fp_U_prime.write(part_lines[0]+'\n')
                fp_U_prime.write(part_lines[1]+'\n')
                fp_U_prime.write(part_lines[2]+'\n')
            else:
                fp_U_out.write(part_lines[0]+'\n')
                fp_U_out.write(part_lines[1]+'\n')
                fp_U_out.write(part_lines[2]+'\n')
                fp_U_out.write(part_lines[3]+'\n')
            fp_pre.write(part_lines[0]+'\n')
            fp_pre.write(part_lines[1]+'\n')
            fp_pre.write(part_lines[2]+'\n')
            fp_pre.write(pre_ret.encode('UTF-8')+'\n')
            ###DONE...
            part_lines = []
    fp_U_in.close()
    os.remove('./after_tag/U.xxx_tmp')
    fp_U_out.close()
    fp_U_prime.close()
    fp_pre.close()
    file_add('./after_tag/L.xxx', './after_tag/U_prime.xxx') # L+U'->L

def drive_iterate():
    global match_count
    cop_file('./after_tag/L_init.xxx', './after_tag/L.xxx')
    cop_file('./after_tag/U_init.xxx', './after_tag/U.xxx')
    iterate_times = 1 #terminate by the iterate_times
    for iterate_i in range(iterate_times):
        single_iterate()
    print 'match_count: %d' % match_count

if __name__ == "__main__":
    start = time.clock()
    pynlpir.open()
    init_rule()
    drive_iterate()
    pynlpir.close()
    end = time.clock()
    print 'Time to run: %f' % (end-start)
