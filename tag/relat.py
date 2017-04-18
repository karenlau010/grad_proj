# -*- coding: utf-8 -*-

import pynlpir
import sys
import re
import os
import json
import time

#decode: str ==> unicode
#encode: unicode ==> str
encode_type = sys.getfilesystemencoding() #UTF-8 in my machine

def relat_pattern():
    fp = file('./pattern/实体之间关系规则.pat', 'rb')
    pat_list = []
    for line in fp:
        line = (line.strip()).decode('UTF-8')
        eles = line.split()
        pat_list.append(eles)
    fp.close()
    return pat_list

def relat_rule():
    texts_list = os.listdir('./after_tag')
    pat_list = relat_pattern()
    for text in texts_list:
        print '>>>>>>>>>>>>>>>>>',
        print text
        if len(re.findall(ur'.*_ner$', text)) > 0:
            pass
        else:
            continue
        fp = file(os.path.join('./after_tag', text), 'rb')
        fp_out = file(os.path.join('./after_tag', text+'_rrule'), 'wb')
        part_no = 4
        count = 0
        part_lines = []
        for line in fp:
            part_lines.append(line.strip())
            count += 1
            if count == 4:
                count = 0
                fp_out.write(part_lines[0]+'\n')
                fp_out.write(part_lines[1]+'\n')
                fp_out.write(part_lines[2]+'\n')
                fp_out.write(part_lines[3]+'\n')
                ne_list = ((part_lines[3].decode('UTF-8')).split())[1:]
                string = part_lines[2].decode('UTF-8')
                relat_list = set()
                for pat_i in range(len(pat_list)):
                    pat_str = pat_list[pat_i][0]
                    relat_type = pat_list[pat_i][1]
                    pattern = re.compile(pat_str)
                    ret_list = pattern.findall(string)
                    if len(ret_list) > 0:
                        print '='*50
                        print part_lines[1]
                        print string.encode('UTF-8')
                        print '命名实体: '+' '.join(y.encode(encode_type) for y in ne_list)
                        print '匹配规则: '+' '.join(y.encode(encode_type) for y in ret_list)
                        ret_list = list(set(ret_list))
                        for ret in ret_list:
                            ne_str_list = re.findall(ur'\[\[.{0,5}<[A-Z]{3}>.{0,5}\d+\]\]', ret)
                            ne_no_list = []
                            for ne_i in ne_str_list:
                                ne_no = re.findall(ur'\d+', ne_i)
                                assert len(ne_no) == 1
                                ne_no = int(ne_no[0])
                                ne_no_list.append(ne_no)
                            for i in range(2, len(pat_list[pat_i])):
                                ne_pair = pat_list[pat_i][i].split('-')
                                assert len(ne_pair) == 2
                                left_ne = ne_no_list[int(ne_pair[0])]
                                right_ne = ne_no_list[int(ne_pair[1])]
                                relat_list.add('<'+str(left_ne)+','+relat_type+','+str(right_ne)+'>')
                        print '实体关系: '+' '.join(y.encode('UTF-8') for y in relat_list)
                fp_out.write('实体关系: '+' '.join(y.encode('UTF-8') for y in relat_list)+'\n')
                part_lines = []
        fp.close()
        fp_out.close()

if __name__ == "__main__":
    relat_rule()
