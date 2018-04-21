#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author:    xurongzhong#126.com
# CreateDate: 2018-1-8 
# check_md5.py

import argparse

import pandas as pd

import servers

parser = argparse.ArgumentParser()
parser.add_argument('labels', action="store", help=u'labels')
parser.add_argument('files', action="store", help=u'测试图片列表文件')
parser.add_argument('scores', action="store", help=u'服务器liveness结果')
parser.add_argument('-s', action="store", dest="score", default=0.7, type=float,
                    help=u'分数的门限')
parser.add_argument('-o', action="store", dest="output",
                    default="live_result.xlsx", help=u'结果输出目录') 
parser.add_argument('--version', action='version',
                    version='%(prog)s 1.0 Rongzhong xu 2018 04 18')
options = parser.parse_args()


values = []

for i in range(18):
    values.append(i*0.05+0.1)
    
    
df_score = pd.read_csv(options.scores, header=None, names=['score'])
df_file = pd.read_csv(options.files, header=None, names=['filename'])
df_label = pd.read_csv(options.labels, header=None, names=['label'])

df = pd.concat([df_label, df_score, df_file], axis=1)

results = []
for value in values:
    result = servers.get_gaze_frr_far(df, 'score', value)
    results.append([value, *result])

df4 = pd.DataFrame(results, columns=["Threshold","number","real_number", "frr_number", "no_number", "far_number","FAR", "FRR"])

df4.to_csv("gaze_far_frr.csv",index=None)