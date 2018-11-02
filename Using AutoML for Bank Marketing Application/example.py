import urllib.request
import zipfile

print("downloading machine-learning-databases")
bank_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip"
bank_filename = "./bank.zip"
bank_additional_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip"
bank_additional_filename = "./bank-additional.zip"
extranct_dir = "./machine-learning-databases-00222/"
upload_file_names = ["bank.csv"]
# bank.csv  bank-full.csv  bank-names.txt

with urllib.request.urlopen(bank_url) as web:
    # 为保险起见使用二进制写文件模式，防止编码错误
    with open(bank_filename, 'wb') as outfile:
        outfile.write(web.read())
f = zipfile.ZipFile(bank_filename, 'r')
for file in f.namelist():
    f.extract(file, extranct_dir)

with urllib.request.urlopen(bank_additional_url) as web:
    # 为保险起见使用二进制写文件模式，防止编码错误
    with open(bank_additional_filename, 'wb') as outfile:
        outfile.write(web.read())
f = zipfile.ZipFile(bank_additional_filename, 'r')
for file in f.namelist():
    f.extract(file, extranct_dir)
print("download & extract machine-learning-databases OK!")

#替换csv文件 分号为逗号(为了适应ModelArts预测功能)
for upfile_name in upload_file_names:
    old = open(extranct_dir+upfile_name, 'r')
    new = open(extranct_dir+'new'+upfile_name, 'w')
    old_replace = ";"
    new_replace = ","
    for i in old:
        if old_replace in i:
            i = i.replace(old_replace,new_replace)
        new.write(i)
    old.close()
    new.close()
else:
    print("替换csv文件 分号为逗号(为了适应ModelArts预测功能)完毕")

# 引入OBS模块
from obs import ObsClient

bucketName = 'model-arts-demo'

try:
    # 创建OBS客户端
    obsClient = ObsClient(
        access_key_id='LGCUKNYSCPHOLEH5UPZP',
        secret_access_key='1g7ttzgdelafd1v6teb1qR2iKqRzJpYQuOwl8rgw',
        server='https://obs.cn-north-1.myhwclouds.com')

    # 创建ObsClient实例
    resp = obsClient.createBucket(bucketName)
    if resp.status < 300:
        print('requestId:', resp.requestId)
    else:
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
        raise Exception('创建桶错误')

    #打开桶版本支持
    resp = obsClient.setBucketVersioning(bucketName, 'Enabled')
    if resp.status < 300:
        print('requestId:', resp.requestId)
    else:
        print('errorCode:', resp.errorCode)
        print('errorMessage:', resp.errorMessage)
        raise Exception('打开桶多版本支持错误')

    #上传训练数据到OBS
    for upfile_name in upload_file_names:
        resp = obsClient.putFile(bucketName, upfile_name, file_path=extranct_dir+'new'+upfile_name)
        if resp.status < 300:
            print('requestId:', resp.requestId)
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            raise Exception(upfile_name+'上传到OBS错误')
    else:
        print("所有文件上传完毕")

    print("可以开始进行预测分析")
    print(bucketName+"obs.cn-north-1.myhwclouds.com")

except Exception as err:
    print(err)
    import traceback
    print(traceback.format_exc())
finally:
    obsClient.close()