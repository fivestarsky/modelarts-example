import urllib.request
import zipfile

# 引入OBS模块
from obs import ObsClient

print("downloading with urllib")

bank_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip"
bank_filename = "./bank.zip"

bank_additional_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip"
bank_additional_filename = "./bank-additional.zip"

extranct_dir = "./machine-learning-databases-00222/"

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



bucketName = 'model-arts-demo'
# 创建ObsClient实例
with ObsClient(
    access_key_id='LGCUKNYSCPHOLEH5UPZP',
    secret_access_key='1g7ttzgdelafd1v6teb1qR2iKqRzJpYQuOwl8rgw',
    server='https://model-arts-demo.obs.cn-north-1.myhwclouds.com'
) as obsClient:
    # 设置桶的多版本状态
    try:
        resp = obsClient.createBucket(bucketName)
        if resp.status < 300:
            print('requestId:', resp.requestId)
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            raise Exception('创建桶错误')

        resp = obsClient.setBucketVersioning(bucketName, 'Enabled')
        if resp.status < 300:
            print('requestId:', resp.requestId)
        else:
            print('errorCode:', resp.errorCode)
            print('errorMessage:', resp.errorMessage)
            raise Exception('打开桶多版本支持错误')
    except:
        import traceback
        print(traceback.format_exc())

    finally:
        obsClient.close()



