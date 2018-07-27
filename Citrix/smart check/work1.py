#coding:utf-8
import nltk
import csv
import os
import string
import datetime
import re
import xlrd

def ReadCSVFile(filepath,encoding='utf-8'):
    data = []
    with open(filepath,'r',encoding=encoding) as f:
        reader = csv.reader((line.replace('\0', '') for line in f))
        for i in reader:
            data.append(i)
    return data

def GetAllCSVPathInOneDir(path):
    csv_file_name = 'issue_key_duration.csv'
    csv_file_path = []
    if not os.path.isdir(path):
        print('Error:"',path,'" is not a directory or does not exist.')
        return
    list_dirs = os.walk(path)
    for root, dirs, files in list_dirs:       #遍历该元组的目录和文件信息
        for f in files:
            if f == csv_file_name:
                csv_file_path.append(os.path.join(root, f))
    return csv_file_path

def GetAllSitePathAndOrgId(path):
    site_path = []
    site_name = os.listdir(path)
    for name in site_name:
        site_path.append([os.path.join(path,name),name])
    return site_path

def GetAllErrDataInOrg(path='../../../info/SmartTool/alldata/report_6.7/tmp/report'):
    path_sit_and_org_name = GetAllSitePathAndOrgId(path)# 该列表每个元素形如['../../../info..../32425','32425]
    all_err_data = []
    for org in path_sit_and_org_name:
        one_org_err_data = []
        org_dir_path = org[0]
        org_id = org[1]
        print(org_id)
        all_csv_path=GetAllCSVPathInOneDir(org_dir_path)
        for csv_path in all_csv_path:
            one_site_data=[]
            all_data = ReadCSVFile(csv_path)
            for i in all_data[1:]:
                if i[3] == 'Error':
                    one_site_data.append([org_id,i[1],i[3],i[4],i[5],i[6]])
            one_org_err_data+=one_site_data
        all_err_data+=one_org_err_data

    with open('newdata.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        # writer.writerow(['Product Component','Subject','Description','Resolution'])
        for x in all_err_data:
            writer.writerow(x)

def GetTranslateData(path='../../../info/SmartTool/alldata/salesforce_vs_sc_account_mapping.xlsx'):
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows #行数
    data={}
    for i in range(nrows):
        rowValues= table.row_values(i) #某一行数据
        if len(rowValues)==2:
            data[rowValues[0]]=rowValues[1]
    return data

def GetIssueData(path='../../../info/SmartTool/alldata/issues_list_new.csv'):
    data = ReadCSVFile(path)
    newdata = []
    for i in data[1:]:
        newdata.append([i[1],i[-2],i[-1]])#[isseu_key,issue_description,issue_resolution]
    return newdata

translate_data = GetTranslateData()
issue_data = GetIssueData()
rule = re.compile(r'\d+')
err_data = ReadCSVFile('newdata.csv')
case_data = ReadCSVFile('../../../info/SmartTool/alldata/48w_ts_cases_from_20160101.csv')
useful_case=[]
ffdata = ReadCSVFile('mydata2.csv')



for i in case_data[1:]:
    if len(i)==20:
        if rule.search(i[-1]):
            case_create_time = datetime.datetime.strptime(i[3], '%Y-%m-%d')
            useful_case.append([i[0],case_create_time,i[-1]])#[case_number,subject,resolution,start_time,org_id]

goal=[]
n=0
m=0
newdata=[]
for i in err_data:#[org_id,issue_key,severity,site_id,begin_time,end_time]
    try:
        m+=1
        print(m)
        start_time = datetime.datetime.strptime(i[4].split(' ')[0],'%Y-%m-%d')
        end_time = datetime.datetime.strptime(i[5].split(' ')[0],'%Y-%m-%d')
        i[4] = start_time
        i[5] = end_time

        for j in range(len(ffdata)):
            if ffdata[j][1] == i[1] and ffdata[j][0]==i[0] and ffdata[j][5]==i[3]:
                ffdata[j][6] = start_time
                ffdata[j][7] = end_time
    except:
        print('err')

    # for j in useful_case:
    #     try:
    #         org_id_j = translate_data[j[2]]
    #     except:
    #         org_id_j = '0'
    #     if i[0] == org_id_j and j[1].__ge__(start_time) and end_time.__ge__(j[1]):
    #         n+=1
    #         print('-----------------------------------------------------------------------------------')
    #         print(n)
    #         print('-----------------------------------------------------------------------------------')
    #         d = i+j
    #         goal.append(d)

with open('mydata0.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    # writer.writerow(['Product Component','Subject','Description','Resolution'])
    for x in ffdata:
        writer.writerow(x)