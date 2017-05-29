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

###should't use the dict(disorder)
rep_dict = [(u"(?:[SYM]<DIS>|<DIS>[SYM]|<DIS>)",u"<DIS>"), (u"(?:<SYM><DIS>|<DIS><SYM>|<SYM>)",u"<SYM>"), (u"<SYM>",u"[SYM]")]
###...

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

def gen_sent(seg_line):
    rule_ret = ""
    pre_pos = ''
    for seg_i in range(len(seg_line)):
        word = seg_line[seg_i][0]
        pos = seg_line[seg_i][1]
        region = seg_line[seg_i][2]
        if pos == 'punctuation-mark' or pos == 'noun' or pos == 'verb': #Maybe add something
            rule_ret += ('#'+word+'/'+word+'@'+str(region[0])+'-'+str(region[1]))
        else:
            if pos[0] != '<' and pos[-1] != '>':
                rule_ret += ('#'+word+'/'+pos+'@'+str(region[0])+'-'+str(region[1]))
            else:
                rule_ret += ('#'+pos+'@'+str(region[0])+'-'+str(region[1]))
        pre_pos = pos
        pre_region = region[:]
    if rule_ret[0] == '#':
        rule_ret = rule_ret[1:]
    return rule_ret

def raw2re_extend_part(re_rule):
    ### re_rule = re.sub("@\d+-\d+", '', re_rule, count=0, flags=0) #This is a switch
    re_rule = re_rule.split('#')
    assert re_rule[0] != u''
    for re_i in range(len(re_rule)):
        re_rule[re_i] = re.sub("^.*/", '', re_rule[re_i], count=1, flags=0) #only retain the tagging
    re_rule = ' '.join(re_rule)
    return re_rule

def extend2re(re_rule):
    global rep_dict
    re_rule = re_rule.split()
    if re_rule[0][0] == '*' or re_rule[0][0] == u'*': #remove the head
        re_rule = re_rule[1:]
    if re_rule[-1][0] == '*' or re_rule[-1][0] == u'*': #remove the tail
        re_rule = re_rule[:-1]
    re_rule = '#'.join(re_rule)
    for k,v in rep_dict:
        re_rule = re_rule.replace(v, k)
    re_rule = re.sub("\*@\d+-\d+", '*', re_rule, count=0, flags=0)
    re_rule = re_rule.replace('*', u'[^，：。;]*')
    re_rule = re_rule.replace(u'#[^，：。;]*', u'[^，：。;]*')
    re_rule = re_rule.replace(u'[^，：。;]*#', u'[^，：。;]*')
    re_rule = re.sub("@\d+-\d+", '@\\d+-\\d+', re_rule, count=0, flags=0)
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
        re_rule = raw2re_extend_part(re_rule)
        re_rule = extend2re(re_rule)
        com_rule = re_rule+' '+re_lest
        if  com_rule not in cur_rule_set:
            fp_re.write('>>> '+(' '.join(raw_rule)).encode('UTF-8')+'\n')
            fp_re.write(com_rule.encode('UTF-8')+'\n')
        cur_rule_set.add(com_rule)
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
    ret_sent = gen_sent(seg_line)
    ret_sent = raw2re_extend_part(ret_sent)
    return ret_sent

def find_region(flag_sent, raw_string):
    sent_parts = flag_sent.split()
    part_head = sent_parts[0]
    part_tail = sent_parts[-1]
    head_num = re.findall(r'\d+', part_head)
    tail_num = re.findall(r'\d+', part_tail)
    assert len(head_num) == 2 and len(tail_num) == 2
    head_num = int(head_num[0])
    tail_num = int(tail_num[1])
    # print raw_string.encode(encode_type)
    # print flag_sent
    # print raw_string[head_num:tail_num].encode(encode_type)
    # print head_num, tail_num
    return (head_num, tail_num)

def match_rule(pre_sent, raw_string):
    global cur_rule_set
    global match_count
    ret_list = []
    for rule_i in cur_rule_set:
        rule_l = rule_i.split()
        rule_part = rule_l[0]
        rule_part = rule_part.replace('#', ' ')
        find_ret = re.findall(rule_part, pre_sent)
        if len(find_ret) > 0:
            for find_i in find_ret:
                new_ret = []
                new_ret.append(find_region(find_i, raw_string)) #the elements of the list is tuple type
                new_ret.append(rule_i)
                ret_list.append(new_ret)
                match_count += 1
    return ret_list

def L2U_init():
    fp_L = file('./after_tag/L_init.xxx', 'rb')
    fp_U = file('./after_tag/U_init.xxx', 'wb')
    part_no = 5
    count = 0
    part_lines = []
    for line in fp_L:
        part_lines.append(line.strip())
        count += 1
        if count == 5:
            count = 0
            fp_U.write(part_lines[0]+'\n')
            fp_U.write(part_lines[1]+'\n')
            fp_U.write(part_lines[2]+'\n')
            fp_U.write(part_lines[3]+'\n')
            part_lines = []
    fp_L.close()
    fp_U.close()

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
            match_short_list = match_rule(pre_ret, raw_string)
            if len(match_short_list) > 0:
                fp_U_prime.write(part_lines[0]+'\n')
                fp_U_prime.write(part_lines[1]+'\n')
                fp_U_prime.write(part_lines[2]+'\n')
                fp_U_prime.write(part_lines[3]+'\n')
                fp_U_prime.write((u'匹配的短句：').encode('UTF-8')+'\n')
                for short_i in match_short_list:
                    short_low, short_high = short_i[0]
                    match_pattern = short_i[1]
                    fp_U_prime.write(match_pattern.encode('UTF-8')+'\n')
                    fp_U_prime.write(raw_string[short_low:short_high].encode('UTF-8')+'\n')
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
    ### L2U_init() #just for test
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
