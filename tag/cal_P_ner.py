# -*- coding: utf-8 -*-

import random

def cal(file_path, file_len, fp_total):
    sample_count = int(file_len * 0.2)
    #print file_len, sample_count
    sample_list = random.sample(range(0, file_len), sample_count)
    #print sample_list
    fp = file(file_path, 'rb')
    fp_out = file(file_path+'_sam', 'wb')
    count = 0
    part_count = 0
    part_lines = []
    for line in fp:
        part_lines.append(line.strip())
        count += 1
        if count == 4:
            print part_count
            if part_count in sample_list:
                fp_out.write(part_lines[0]+'\n')
                fp_out.write(part_lines[1]+'\n')
                fp_out.write(part_lines[2]+'\n')
                fp_out.write(part_lines[3]+'\n')
                fp_total.write(part_lines[0]+'\n')
                fp_total.write(part_lines[1]+'\n')
                fp_total.write(part_lines[2]+'\n')
                fp_total.write(part_lines[3]+'\n')
            part_count += 1
            count = 0
            part_lines = []
    fp.close()
    fp_out.close()

def wrong_count():
    fp = file('total_sample.txt_save', 'rb')
    count = 0
    wrong_count = 0
    part_lines = []
    for line in fp:
        part_lines.append(line.strip())
        count += 1
        if count == 4:
            ne_list = ((part_lines[3].decode('UTF-8')).split())[1:]
            if ne_list[-1] == 'x':
                wrong_count += 1
            count = 0
            part_lines = []
    fp.close()
    print wrong_count

if __name__ == "__main__":
    file_list = {u"中国高血压防治指南_.txt_mm_ner_eval":401, u"心房颤动 目前认识和治疗建议.txt_mm_ner_eval":1002, u"室性心律失常药物治疗选择_蒋文平.txt_mm_ner_eval":242, u"儿童常见先天性心脏病介入治疗专家共识.txt_mm_ner_eval":243, u"常见先天性心脏病介入治疗中国专家共识一、房间隔缺损介入治疗.txt_mm_ner_eval":186, u"常见先天性心脏病介入治疗中国专家共识五、先天性心脏病复合畸形的介入治疗.txt_mm_ner_eval":194, u"常见先天性心脏病介入治疗中国专家共识四、经皮球囊肺动脉瓣与主动脉瓣成形术.txt_mm_ner_eval":217, u"常见先天性心脏病介入治疗中国专家共识三、动脉导管未闭的介入治疗.txt_mm_ner_eval":89, u"常见先天性心脏病介入治疗中国专家共识二、室间隔缺损介入治疗.txt_mm_ner_eval":136}
    '''
    fp_total = file('total_sample.txt', 'wb')
    for k,v in file_list.iteritems():
        cal(k, v, fp_total)
    fp_total.close()
    '''
    wrong_count()