import pymongo

# Kết nối tới MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Tạo hoặc chọn cơ sở dữ liệu
mydb = myclient["2174802010439"]

# Tạo hoặc chọn bảng (collection) để lưu trữ dữ liệu
collection = mydb["population"]

# Truy vấn để lấy danh sách các giá trị duy nhất trong trường "Location"
locations = collection.distinct("Location")

# In danh sách các khu vực theo format yêu cầu
print("Danh sách các khu vực có trong trường 'Location':")
print(", ".join(f'"{location}"' for location in locations))
