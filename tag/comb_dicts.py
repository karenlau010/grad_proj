# -*- coding: utf-8 -*-

import os
import json

#decode: str ==> unicode
#encode: unicode ==> str

def comb_dicts(base_path, dicts_list, targ_name):
    comb_set = set()
    total_count = 0
    print "="*30
    for d in dicts_list:
        word_count = 0
        fp = file(os.path.join(base_path, d), 'rb')
        for word in fp:
            word_count += 1
            comb_set.add((word.strip()).decode("UTF-8"))
        fp.close()
        total_count += word_count
        print "%s: %d" % (d, word_count)
    print "total: %d" % total_count
    print "%s: %d" % (targ_name, len(comb_set))
    fp_out = file(targ_name, 'wb')
    comb_list = list(comb_set)
    comb_list.sort()
    for word in comb_list:
        fp_out.write(word.encode("UTF-8")+'\n')
    fp_out.close()

def clean_dict(filename):
    fp = file(filename+'_raw', 'rb')
    fp_may = file('./dictionary/药品_可能.dic', 'wb')
    fp_chm = file('./dictionary/中草药.dic', 'rb')
    chm_dict = set()
    for chm in fp_chm:
        chm = (chm.strip()).decode('UTF-8')
        chm_dict.add(chm)
    fp_out = file(filename, 'wb')
    postfix = [u'公司', u'厂', u'生产', u'医药部', u'研究所', u'集团', u'责任司', u'责任公', u'制药', u'代理商', u'有限公', u'国药', u'会社', u'分装', u'中心', u'代理', u'包装', u'制造所', u'工场', u'公示', u'股份', u'药业', u'意大利', u'日本', u'工司', u'公司无', u'天银制', u'公司委', u'年月止', u'期自', u'韩国', u'香港', u'法', u'毫升', u'口服', u'次', u'疗程', u'盒', u'学会', u'器', u'瓶', u'管', u'针', u'制', u'瘤', u'增生', u'突起', u'移位', u'肌', u'体', u'小', u'病', u'瓣', u'狭窄', u'植物', u'生长', u'移植', u'愈合', u'缝合', u'者', u'假说', u'分压', u'固定', u'容量', u'施肥', u'张力', u'图', u'浴', u'点', u'麻醉', u'进口', u'兽', u'创可贴', u'对照品', u'相', u'共生', u'异构', u'痣', u'反应', u'化', u'欲', u'积水', u'力', u'因子', u'计划', u'图谱', u'发生', u'单位', u'模具', u'失禁', u'板', u'带', u'测压', u'性', u'计', u'标记', u'扫描', u'装置', u'学说', u'时间', u'流动', u'曲线', u'体积', u'名称', u'遗传', u'部', u'所', u'隔离', u'流', u'式', u'畸形', u'道', u'房', u'曲', u'山', u'修复', u'破裂', u'支持', u'系统', u'量', u'压', u'胸', u'框', u'检', u'识别', u'效应', u'瓣膜', u'值', u'系', u'痒', u'造影', u'梗阻', u'病变', u'结核', u'瘘', u'脱落', u'吻合', u'闭锁', u'过多', u'裂', u'刀', u'疣', u'治疗', u'比对', u'缺血', u'序列', u'异常', u'免疫', u'突变', u'螺旋', u'溃疡', u'曲张', u'扩张', u'褶', u'束', u'传导', u'测', u'症', u'数', u'风险', u'吸取', u'钳', u'检查', u'疮', u'斑', u'疹', u'模拟', u'度', u'缺陷', u'感染', u'污染', u'培养', u'本质', u'转移', u'机', u'纤维', u'组织', u'识别卡', u'栓', u'结石', u'淤积', u'疝', u'分类', u'矩阵', u'重组', u'微笑', u'癜', u'器官', u'词', u'词尾', u'确切', u'作用', u'神经', u'尿', u'发育', u'机理', u'尿', u'息肉', u'诊断', u'小儿', u'国产', u'痉挛', u'状态', u'镜', u'尺', u'率', u'数据']
    prefix = [u'一次', u'一种', u'先天', u'上皮', u'龈', u'龋失', u'交叉', u'冠状', u'农业', u'微笑', u'后天']
    for med in fp:
        med = (med.strip()).decode('UTF-8')
        if med in chm_dict: #delete the chm
            #fp_may.write(med.encode('UTF-8')+'\n')
            pass
        elif med[-2:] in postfix or med[-1:] in postfix or med[-3:] in postfix or \
                med[:2] in prefix:
            fp_may.write(med.encode('UTF-8')+'\n')
            pass
        else:
            fp_out.write(med.encode('UTF-8')+'\n')
    fp.close()
    fp_out.close()
    fp_may.close()

def clean_39net_sym():
    fp = file('./dictionary/dict/symptom_39net.txt_raw', 'rb')
    fp_out = file('./dictionary/dict/symptom_39net.txt', 'wb')
    for word in fp:
        if word[-4:-1] != '...':
            fp_out.write(word)
    fp.close()
    fp_out.close()

if __name__ == "__main__":
    base_path = './dictionary/dict'
    #clean_dict('./dictionary/dict/医药名称.scel.txt_UTF-8')
    #comb_dicts(base_path, ['symptom_39net_part1.txt', 'symptom_39net_part2.txt', 'symptom_39net_part3.txt'], './dictionary/dict/symptom_39net.txt_old')
    #clean_39net_sym()
    #comb_dicts(base_path, ['download_cell.scel.txt_UTF-8', '医药公司大全.scel.txt_UTF-8', '常用药品生产厂家的名称.scel.txt_UTF-8', '药品产地.scel.txt_UTF-8', '药品生产企业词库.scel.txt_UTF-8'], './dictionary/药品生产企业.dic')
    #comb_dicts(base_path, ['ffd.scel.txt_UTF-8', '中草药.scel.txt_UTF-8', '中药名称.scel.txt_UTF-8', '中药名称ab.scel.txt_UTF-8', '中药名称词库.scel.txt_UTF-8', '中药药材.scel.txt_UTF-8', '中药饮片.scel.txt_UTF-8', '中药材及部分中药饮片.scel.txt_UTF-8', '中药词汇.scel.txt_UTF-8', '部分中药材词库.scel.txt_UTF-8', '常用中药名.scel.txt_UTF-8', '快速输入中药名称.scel.txt_UTF-8', '药店中药饮片410个.scel.txt_UTF-8', '独活的中药词库-健康是福-急毒药材132味.scel.txt_UTF-8', '常用中药处方名称（唐都医院中医科丁井永）.scel.txt_UTF-8'], './dictionary/中草药.dic')
    #comb_dicts(base_path, ['医疗仪器与医疗器械.scel.txt_UTF-8', '医疗器械大全【官方推荐】.scel.txt_UTF-8', '医疗器材及试剂词库.scel.txt_UTF-8', '公司专用器械.scel.txt_UTF-8', 'yiyongqixie.com.txt', 'medsoso.cn.txt'], './dictionary/医学器械.dic')
    #comb_dicts(base_path, ['医药化工字典.scel.txt_UTF-8', '精神药物.scel.txt_UTF-8', '药品对照品.scel.txt_UTF-8', '部分的西药名称.scel.txt_UTF-8', '维康医院西药目录.scel.txt_UTF-8', '医院西药名称.scel.txt_UTF-8', '医药名称.scel.txt_UTF-8', '中外药品名称大全【官方推荐】.scel.txt_UTF-8', '临床用药大全STZ.scel.txt_UTF-8', '处方常用药品通用名目录.scel.txt_UTF-8', '心血管内科常用药.txt'], './dictionary/药品.dic_raw')
    #comb_dicts(base_path, ['医药化工字典.scel.txt_UTF-8', '精神药物.scel.txt_UTF-8', '药品对照品.scel.txt_UTF-8', '部分的西药名称.scel.txt_UTF-8', '维康医院西药目录.scel.txt_UTF-8', '医院西药名称.scel.txt_UTF-8', '临床用药大全STZ.scel.txt_UTF-8', '处方常用药品通用名目录.scel.txt_UTF-8', '心血管内科常用药.txt'], './dictionary/药品.dic_raw') # have not '医药名称.scel.txt_UTF-8', '中外药品名称大全【官方推荐】.scel.txt_UTF-8'
    #clean_dict('./dictionary/药品.dic')
    comb_dicts(base_path, ['手术分类与代码(ICD-9-CM3).scel.txt_UTF-8', '国际标准手术编码.scel.txt_UTF-8', 'baidu百科_心脏介入手术.txt', 'a-hospital.com_胸心外科手术.txt', 'a-hospital.com_血管外科手术.txt', 'a-hospital.com_临床常用诊断技术.txt'], './dictionary/手术检查.dic')
    #comb_dicts(base_path, ['ICD-10疾病编码1.scel.txt_UTF-8', '西医病名.scel.txt_UTF-8', '飞华健康网_心血管内科疾病.txt'], './dictionary/疾病.dic')
    comb_dicts(base_path, ['症状名.scel.txt_UTF-8', 'symptom_39net.txt', 'symptom_120net.txt', '飞华健康网_心脏症状.txt', '飞华健康网_症状.txt', '心电图诊断用语.scel.txt_UTF-8', 'qiuyi.cn_sym.txt'], './dictionary/症状.dic')
    comb_dicts(base_path, ['心血管内科常用药.txt', 'a-hospital.com_治疗心脑血管疾病的药品列表.txt', 'a-hospital.com_治疗病毒性心肌炎的药品列表.txt', 'a-hospital.com_其它治疗心脑血管疾病的药品列表_part1.txt', 'a-hospital.com_其它治疗心脑血管疾病的药品列表_part2.txt', 'a-hospital.com_治疗高血压的药品列表.txt', 'a-hospital.com_治疗冠心病的药品列表.txt', 'a-hospital.com_治疗心力衰竭的药品列表.txt', 'a-hospital.com_治疗心绞痛的药品列表.txt', 'a-hospital.com_治疗心肌病的药品列表.txt', 'a-hospital.com_治疗高血脂的药品列表.txt', 'a-hospital.com_治疗心功能不全的药品列表_part1.txt', 'a-hospital.com_治疗心功能不全的药品列表_part2.txt', 'a-hospital.com_治疗动脉硬化的药品列表.txt', 'a-hospital.com_治疗肺动脉高压的药品列表.txt', 'a-hospital.com_治疗心慌心悸的药品列表.txt', 'a-hospital.com_治疗中风和偏瘫的药品列表.txt', 'a-hospital.com_治疗胸闷和胸痛的药品列表.txt', 'a-hospital.com_治疗心律失常的药品列表.txt', 'a-hospital.com_治疗心律失常的药品列表_part2.txt', 'a-hospital.com_ATC代码_C心血管系统.txt', 'a-hospital.com_ATC代码_B血液系统.txt', 'a-hospital.com_心血管系统常见药剂类别.txt', 'www.baikemy.com_药品.txt'], './dictionary/药物.dic')
    comb_dicts(base_path, ['飞华健康网_心血管内科疾病.txt', 'a-hospital.com_心血管内科疾病_part1.txt', 'a-hospital.com_心血管内科疾病_part2.txt', 'a-hospital.com_心血管内科疾病_part3.txt', 'jbk.99.com.cn_心血管内科疾病大全.txt', 'cndzys.com_心血管内科相关疾病.txt', '西医病名.scel.txt_UTF-8', 'ICD-10疾病编码1.scel.txt_UTF-8'], './dictionary/疾病.dic')
    #comb_dicts(base_path, ['baidu百科_心脏介入手术.txt', 'a-hospital.com_胸心外科手术.txt', 'a-hospital.com_血管外科手术.txt', 'a-hospital.com_临床常用诊断技术.txt'], './dictionary/心血管相关手术.dic')
