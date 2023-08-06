import pymongo
import pandas as pd

#Kết nối vào mongodb
myClient = pymongo.MongoClient('mongodb://localhost:27107/')

#Liên kết với database
mydb = myClient['2174802010439']

#Tạo hoặc chọn collection
collection = mydb['population']

#Liên kết tới file csv
file_path = 'WPP2022_TotalPopulationBySex.csv'

#Đọc dữ liệu file csv và chuyển đổi thành file JSON
data = pd.read_csv(file_path).to_dict(orient="records")

#Kiểm tra dữ liệu có trong csv không
if data:
    #Chèn dữ liệu vào database
    result = collection.insert_many(data)
    print(f'Đã import thành công {len(result.inserted_ids)}')
else:
    print("Dữ liệu không có trongfile csv")