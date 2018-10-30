import urllib.request
import zipfile



print("downloading with urllib")

bank_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip"
bank_filename = "./bank.zip"
bank_dir = "./bank/"

bank_additional_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip"
bank_additional_filename = "./bank-additional.zip"
bank_additional_dir = "./bank-additional/"


with urllib.request.urlopen(bank_url) as web:
    # 为保险起见使用二进制写文件模式，防止编码错误
    with open(bank_filename, 'wb') as outfile:
        outfile.write(web.read())
f = zipfile.ZipFile(bank_filename, 'r')
for file in f.namelist():
    f.extract(file, bank_dir)


with urllib.request.urlopen(bank_additional_url) as web:
    # 为保险起见使用二进制写文件模式，防止编码错误
    with open(bank_additional_filename, 'wb') as outfile:
        outfile.write(web.read())
f = zipfile.ZipFile(bank_additional_filename, 'r')
for file in f.namelist():
    f.extract(file, bank_additional_dir)


# print("downloading with " + bank_url)
# LocalPath = os.path.join('./', bank_filename)
# urllib.request.urlretrieve(bank_url, LocalPath)
#
#
# print("downloading with " + bank_additional_url)
# LocalPath = os.path.join('./', bank_additional_filename)
# urllib.request.urlretrieve(bank_additional_url, LocalPath)
#
