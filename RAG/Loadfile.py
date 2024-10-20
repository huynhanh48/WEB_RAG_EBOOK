import csv
import re

def loadfilecsv(path: str):
    array = []
    with open(path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            dictnew = {"id": index}
            dictnew.update(row)
            # Loại bỏ ký tự xuống dòng trong 'content'
            dictnew['content'] = re.sub(r'\n', '', dictnew['content']).strip()
            array.append(dictnew)
    return array

def convertDocument(ds: list):
    newlist = []
    for i in ds:
        # Tạo chuỗi mới với các giá trị từ từ điển
        strnew = "id: " + str(i['id']) + ", " + "title: " + i['title'] + ", " + "content: " + i['content'] + ", " + "price: " + i['price']
        newlist.append(strnew)
    return newlist

