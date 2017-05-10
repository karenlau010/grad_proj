# -*- coding: utf-8 -*-

import pynlpir
import sys
import re
import os
import time

#decode: str ==> unicode
#encode: unicode ==> str

ne_pare_list = []

def read_seed(seed_path):
    global ne_pare_list
    fp = file(seed_path, 'rb')
    fp_out = file('./after_tag/seed_pare.xxx', 'wb')
    count = 0
    part_lines = []
    ne_pare_set = set()
    for line in fp:
        part_lines.append(line.strip())
        count += 1
        if count == 5:
            count = 0
            ne_list = ((part_lines[3].decode('UTF-8')).split())[1:]
            relat_list = ((part_lines[4].decode('UTF-8')).split())[1:]
            for r_i in range(len(relat_list)):
                new_relat = relat_list[r_i][:]
                relat_type = re.findall(ur',.*,', new_relat)
                assert len(relat_type) == 1
                relat_type = relat_type[0][1:-1]
                no_pare = re.findall(ur'\d+', new_relat)
                assert len(no_pare) == 2
                new_relat = ne_list[int(no_pare[0])] + ' ' + ne_list[int(no_pare[1])] + ' ' + relat_type
                ne_pare_set.add(new_relat)
            part_lines = []
    ne_pare_list = list(ne_pare_set)
    ne_pare_list.sort()
    for np_i in range(len(ne_pare_list)):
        fp_out.write(ne_pare_list[np_i].encode('UTF-8')+'\n')
        ne_pare_list[np_i] = ne_pare_list[np_i].split()
    fp.close()
    fp_out.close()

def fetch_context():
    global ne_pare_list
    texts_list = os.listdir('./after_tag')
    fp_context = file('./after_tag/pare_context.xxx', 'wb')
    for text in texts_list:
        if len(re.findall(ur'.*_rrule$', text)) > 0:
            pass
        else:
            continue
        fp = file(os.path.join('./after_tag', text), 'rb')
        count = 0
        part_lines = []
        for line in fp:
            part_lines.append(line.strip())
            count += 1
            if count == 5:
                count = 0
                ne_list = ((part_lines[3].decode('UTF-8')).split())[1:]
                for ne_pare in ne_pare_list:
                    ne_left = ne_pare[0]
                    ne_right = ne_pare[1]
                    if ne_left in ne_list and ne_right in ne_list:
                        fp_context.write(part_lines[0]+'\n')
                        fp_context.write(part_lines[1]+'\n')
                        fp_context.write(part_lines[2]+'\n')
                        fp_context.write(part_lines[3]+'\n')
                        fp_context.write(part_lines[4]+'\n')
                part_lines = []
        fp.close()
    fp_context.close()

def deal_cws(in_str):
    seg_line = pynlpir.segment(in_str, pos_tagging=True)
    for s_i in range(len(seg_line)-1, -1, -1):
        seg_line[s_i] = list(seg_line[s_i])
        if seg_line[s_i][1] == None:
            seg_line[s_i][1] = u'None'
            #if seg_line[s_i][0] == u' ': #Attention: can't skip the blank-space
            #    del seg_line[s_i]
        else:
            seg_line[s_i][1] = seg_line[s_i][1].replace(' ', '-')
    cur_pos = 0
    for s_i in range(len(seg_line)):
        ne_pos_pare = []
        ne_pos_pare.append(cur_pos)
        cur_pos += len(seg_line[s_i][0])
        ne_pos_pare.append(cur_pos)
        seg_line[s_i].append(ne_pos_pare)
    ###seg_line = ' '.join('/'.join(y) for y in seg_line)
    return seg_line

def cal_ne_pos(in_str, ne_list):
    cur_pos = 0
    is_i = 0
    no_str = ''
    ne_type = ''
    ne_pos_list = []
    while is_i < len(in_str):
        char = in_str[is_i]
        if char == '[':
            if is_i < (len(in_str) - 1):
                is_i += 1
                char = in_str[is_i]
                if char == '[':
                    is_i += 1
                    char = in_str[is_i]
                    while not (char >= u'0' and char <= u'9'):
                        ne_type += char
                        is_i += 1
                        char = in_str[is_i]
                    while char != ']':
                        no_str += char
                        is_i += 1
                        char = in_str[is_i]
                    is_i += 1
                    char = in_str[is_i]
                    assert char == ']'
                    ne_pos_pare = []
                    ne_pos_pare.append(cur_pos)
                    cur_pos += len(ne_list[int(no_str)])
                    ne_pos_pare.append(cur_pos)
                    ne_pos_pare.append(ne_type)
                    ne_pos_list.append(ne_pos_pare)
                    cur_pos -= 1
                    no_str = ''
                    ne_type = ''
                else:
                    is_i -= 1
        is_i += 1
        cur_pos += 1
    return ne_pos_list

def comb_ne_cws(seg_line, ne_pos_list):
    sl_i = 0
    npl_i = 0
    ne_low = ne_pos_list[0][0]
    ne_high = ne_pos_list[0][1]
    cur_low = seg_line[0][2][0]
    cur_high = seg_line[0][2][1]
    low_i = -1
    high_i = -1
    while sl_i < len(seg_line) and npl_i < len(ne_pos_list):
        while cur_low < ne_low:
            sl_i += 1
            if sl_i < len(seg_line):
                cur_low = seg_line[sl_i][2][0]
                cur_high = seg_line[sl_i][2][1]
            else:
                break
        assert sl_i <= len(seg_line)
        if sl_i == len(seg_line):
            break
        if cur_low == ne_low:
            low_i = sl_i
            while cur_high < ne_high:
                sl_i += 1
                cur_high = seg_line[sl_i][2][1]
                cur_low = seg_line[sl_i][2][0]
            if cur_high == ne_high: ###succeed...
                high_i = sl_i
                ###TODO...
                ne_str = ''
                for lh_i in range(high_i, low_i-1, -1):
                    ne_str = seg_line[lh_i][0] + ne_str
                    del seg_line[lh_i]
                ne_type = ne_pos_list[npl_i][2]
                new_part = []
                new_part.append(ne_str)
                new_part.append(ne_type)
                new_part.append(ne_pos_list[npl_i][:2])
                seg_line.insert(low_i, new_part)
                sl_i -= (high_i - low_i) #Attention: don't forget this point
                sl_i += 1
                npl_i += 1
                if npl_i < len(ne_pos_list):
                    ne_low = ne_pos_list[npl_i][0]
                    ne_high = ne_pos_list[npl_i][1]
                if sl_i < len(seg_line):
                    cur_low = seg_line[sl_i][2][0]
                    cur_high = seg_line[sl_i][2][1]
                print ne_low, ne_high, cur_low, cur_high
                ###DONE...
                low_i = -1
                high_i = -1
            else: ###fail...
                while ne_low < cur_high:
                    ###print 'There is a ne can\'t be recognize...111'
                    npl_i += 1
                    if npl_i < len(ne_pos_list):
                        ne_low = ne_pos_list[npl_i][0]
                        ne_high = ne_pos_list[npl_i][1]
                    else:
                        break
        else: ###fail...
            ###print 'There is a ne can\'t be recognize...222'
            while ne_low < cur_low:
                npl_i += 1
                if npl_i < len(ne_pos_list):
                    ne_low = ne_pos_list[npl_i][0]
                    ne_high = ne_pos_list[npl_i][1]
                else:
                    break
    return seg_line

def generalize():
    fp = file('./after_tag/seed_context.xxx', 'rb')
    fp_out = file('./after_tag/seed_generalize.xxx', 'wb')
    count = 0
    part_lines = []
    for line in fp:
        part_lines.append(line.strip())
        count += 1
        if count == 5:
            count = 0
            ne_list = ((part_lines[3].decode('UTF-8')).split())[1:]
            relat_list = ((part_lines[4].decode('UTF-8')).split())[1:]
            raw_string = ((part_lines[1]).strip()).decode('UTF-8')
            tag_string = ((part_lines[2]).strip()).decode('UTF-8')
            ###TODO...compare part
            seg_line = deal_cws(raw_string)
            ne_pos_list = cal_ne_pos(tag_string, ne_list)
            seg_line = comb_ne_cws(seg_line, ne_pos_list)
            #############
            fp_out.write(part_lines[0]+'\n')
            fp_out.write(part_lines[1]+'\n')
            fp_out.write(part_lines[2]+'\n')
            fp_out.write(part_lines[3]+'\n')
            fp_out.write(part_lines[4]+'\n')
            fp_out.write((u'句子划分:').encode('UTF-8'))
            for seg_part in seg_line:
                fp_out.write(' '+(seg_part[0]).encode('UTF-8')+\
                            '/'+str(seg_part[2][0])+'-'+str(seg_part[2][1]))
                #fp_out.write(' '+(seg_part[0]).encode('UTF-8')+'/'+(seg_part[1]).encode('UTF-8')+\
                #            '/'+str(seg_part[2][0])+'-'+str(seg_part[2][1]))
            fp_out.write('\n')
            fp_out.write((u'实体下标:').encode('UTF-8'))
            for ne_pare in ne_pos_list:
                fp_out.write(' ' + str(ne_pare[0]) + '-' + str(ne_pare[1]) + '-' + ne_pare[2])
            fp_out.write('\n')
            ###DONE...
            part_lines = []
    fp.close()
    fp_out.close()

if __name__ == "__main__":
    pynlpir.open()
    seed_path = u'./after_tag/seed_context.xxx'
    read_seed(seed_path)
    fetch_context()
    generalize()
    pynlpir.close()
