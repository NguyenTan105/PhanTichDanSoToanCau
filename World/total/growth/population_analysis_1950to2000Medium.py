import pymongo
import pandas as pd

# Kết nối tới MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Tạo hoặc chọn cơ sở dữ liệu
mydb = myclient["2174802010439"]

# Tạo hoặc chọn bảng (collection) để lưu trữ dữ liệu
collection = mydb["population"]

# Truy vấn để lấy các bản ghi có kịch bản (variant) là "Medium" và các năm trong danh sách năm cho trước
years = [1950, 2000]
query = {
    "Variant": "Medium",
    "Time": {"$in": years}
}

# Lấy dữ liệu từ MongoDB và đưa vào DataFrame
data = list(collection.find(query, {"_id": 0}))
df = pd.DataFrame(data)

# Tính tổng dân số "PopMale" và "PopFemale" của tất cả khu vực "Location" cho các năm trong danh sách năm
total_popmale = df.groupby("Time")["PopMale"].sum()
total_popfemale = df.groupby("Time")["PopFemale"].sum()

# Tính số lượng và phần trăm đã tăng lên giữa các năm trong danh sách năm
popmale_growth_count = total_popmale[years[-1]] - total_popmale[years[0]]
popfemale_growth_count = total_popfemale[years[-1]] - total_popfemale[years[0]]

popmale_growth_percent = (popmale_growth_count / total_popmale[years[0]]) * 100
popfemale_growth_percent = (popfemale_growth_count / total_popfemale[years[0]]) * 100

# In kết quả tổng dân số và phần trăm tăng trưởng qua console log
print(f"Phần trăm tăng trưởng 'PopMale' từ năm {years[0]} đến {years[-1]}: {popmale_growth_percent:.2f}%")
print(f"Phần trăm tăng trưởng 'PopFemale' từ năm {years[0]} đến {years[-1]}: {popfemale_growth_percent:.2f}%")