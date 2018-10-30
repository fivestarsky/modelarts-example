import os
import urllib

print("downloading with urllib")

bank_filename = "bank.zip"
bank_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank.zip"
bank_additional_filename = "bank-additional.zip"
bank_additional_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip"

print("downloading with " + bank_url)
LocalPath = os.path.join('./', bank_filename)
urllib.request.urlretrieve(bank_url, LocalPath)


print("downloading with " + bank_additional_url)
LocalPath = os.path.join('./', bank_additional_filename)
urllib.request.urlretrieve(bank_additional_url, LocalPath)

