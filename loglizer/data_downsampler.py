import os, csv, tqdm

dataDir = '../data/HDFS'
dataFile = '../data/HDFS/syslog.log_structured.csv'

def data_downsample(dataFile, newName, newSize):
    oriData = open(dataFile, 'r')
    newData = open(os.path.join(dataDir, newName), 'w')
    reader = csv.reader(oriData, delimiter=',')
    writer = csv.writer(newData, delimiter=',')

    cnt = 0
    for row in tqdm.tqdm(reader):
        if cnt >= newSize:
            break
        writer.writerow(row)
        cnt += 1

if __name__ == "__main__":
    data_downsample(dataFile, 'syslog_200000.log_structed.csv', 200000)