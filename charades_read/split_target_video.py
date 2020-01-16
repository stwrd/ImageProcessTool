import csv
with open('/media/hzh/ssd_disk/BaiduNetdiskDownload/Charades/Charades/Charades_v1_test.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        actions = row['actions'].split(';')