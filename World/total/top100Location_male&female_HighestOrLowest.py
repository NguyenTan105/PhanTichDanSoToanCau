import pymongo
import pandas as pd

# Kết nối tới MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Tạo hoặc chọn cơ sở dữ liệu
mydb = myclient["2174802010439"]

# Tạo hoặc chọn bảng (collection) để lưu trữ dữ liệu
collection = mydb["population"]

# Truy vấn để lấy các bản ghi có kịch bản (variant) là "Medium"
query = {"Variant": "Medium"}

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', None)

# Lấy dữ liệu từ MongoDB và đưa vào DataFrame
df = pd.DataFrame(list(collection.find(query, {"_id": 0})))

# Thêm cột "Year" vào DataFrame để lưu trữ thông tin năm từ trường "Time"
df["Year"] = df["Time"]

# Tính tổng dân số của từng khu vực theo từng năm
df_grouped = df.groupby(["Location", "Year"])["PopTotal"].sum().reset_index()

# Bắt đầu đánh số từ 1
df_grouped.index += 1

# In danh sách các năm có trong dữ liệu
years_available = df_grouped["Year"].unique()
print("Các năm có trong dữ liệu:", years_available)

# Cho phép người dùng chọn năm từ bàn phím
selected_year = int(input("Nhập năm muốn xem (từ 1950 đến 2023): "))
if selected_year not in years_available:
    print(f"Năm {selected_year} không có trong dữ liệu.")
else:
    # Lọc dữ liệu theo năm đã chọn
    df_selected_year = df_grouped[df_grouped["Year"] == selected_year]

    # Sắp xếp DataFrame theo trường "PopTotal" để tìm 100 khu vực có tổng dân số nhỏ nhất và lớn nhất
    df_sorted = df_selected_year.sort_values(by="PopTotal")

    # Lấy 100 khu vực có tổng dân số nhỏ nhất
    smallest_100_locations = df_sorted.head(100).reset_index(drop=True)

    # Lấy 100 khu vực có tổng dân số lớn nhất và sắp xếp từ lớn đến bé
    largest_100_locations = df_sorted.tail(100).sort_values(by="PopTotal", ascending=False).reset_index(drop=True)

    # # Định dạng đầu ra cho số dấu phẩy động
    # pd.options.display.float_format = '{:,.0f}'.format

    # Bắt đầu đánh số từ 1
    smallest_100_locations.index += 1
    largest_100_locations.index += 1

    # In kết quả
    print(f"100 khu vực có tổng dân số nhỏ nhất với kịch bản (variant: medium) trong năm {selected_year}:")
    print(smallest_100_locations)

    print(f"\n100 khu vực có tổng dân số lớn nhất với kịch bản (variant: medium) trong năm {selected_year}:")
    print(largest_100_locations)
