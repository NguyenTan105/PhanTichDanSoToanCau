import pymongo
import pandas as pd

# Kết nối tới MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Tạo hoặc chọn cơ sở dữ liệu
mydb = myclient["2174802010439"]

# Tạo hoặc chọn bảng (collection) để lưu trữ dữ liệu
collection = mydb["population"]

# Tên file CSV chứa dữ liệu
file_path = "WPP2022_TotalPopulationBySex.csv"

# Đọc dữ liệu từ file CSV và chuyển đổi thành định dạng JSON
data = pd.read_csv(file_path).to_dict(orient="records")

# Kiểm tra xem có dữ liệu trong file CSV không
if data:
    # Chèn dữ liệu vào cơ sở dữ liệu
    result = collection.insert_many(data)
    print(f"Đã import thành công {len(result.inserted_ids)} mục.")
else:
    print("File CSV không có dữ liệu.")
