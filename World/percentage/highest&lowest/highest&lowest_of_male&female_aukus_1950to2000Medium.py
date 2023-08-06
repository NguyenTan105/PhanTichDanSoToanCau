import pymongo
import pandas as pd

# Kết nối tới MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Tạo hoặc chọn cơ sở dữ liệu
mydb = myclient["2174802010439"]

# Tạo hoặc chọn bảng (collection) để lưu trữ dữ liệu
collection = mydb["population"]

# Truy vấn để lấy danh sách các khu vực "Location" có trong dữ liệu
available_locations = collection.distinct("Location")

#Set số lượng tối đa hàng và cột được in ra
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 5)

# Hàm kiểm tra xem một chuỗi có phải là số hay không
def is_number(input_str):
    try:
        int(input_str)
        return True
    except ValueError:
        return False

def calculate(location):
    # Lấy dữ liệu từ MongoDB theo yêu cầu (khu vực, variant "medium", năm từ 1950 đến 2000)
    data = list(collection.find({
        "Location": location,
        "Variant": "Medium",
        "Time": {"$gte": 1950, "$lte": 2000}
    }))

    df = pd.DataFrame(data)

    # Tính phần trăm tăng trưởng dân số cho "popmale" và "popfemale" theo từng năm
    df['PopMale_Growth_Rate'] = df['PopMale'].pct_change() * 100
    df['PopFemale_Growth_Rate'] = df['PopFemale'].pct_change() * 100
   
   # Tìm năm có tốc độ tăng trưởng cao nhất và thấp nhất cho "popmale" và "popfemale"
    max_popmale_growth_year = df.loc[df['PopMale_Growth_Rate'].idxmax(), 'Time']
    min_popmale_growth_year = df.loc[df['PopMale_Growth_Rate'].idxmin(), 'Time']
    max_popfemale_growth_year = df.loc[df['PopFemale_Growth_Rate'].idxmax(), 'Time']
    min_popfemale_growth_year = df.loc[df['PopFemale_Growth_Rate'].idxmin(), 'Time']

    # Xuất kết quả thông tin tốc độ tăng trưởng cao nhất và thấp nhất qua console log
    print(f"Tăng trưởng dân số PopMale cao nhất: {df['PopMale_Growth_Rate'].max():.2f}% vào năm {max_popmale_growth_year}")
    print(f"Tăng trưởng dân số PopMale thấp nhất: {df['PopMale_Growth_Rate'].min():.2f}% vào năm {min_popmale_growth_year}")
    print(f"Tăng trưởng dân số PopFemale cao nhất: {df['PopFemale_Growth_Rate'].max():.2f}% vào năm {max_popfemale_growth_year}")
    print(f"Tăng trưởng dân số PopFemale thấp nhất: {df['PopFemale_Growth_Rate'].min():.2f}% vào năm {min_popfemale_growth_year}")
    print(f"Đây là tốc độ tăng trưởng cao nhất và thấp nhất của khu vực {location} (Variant: Medium) từ 1950 đến 2000")

# Hiển thị danh sách các khu vực có sẵn để người dùng lựa chọn
print("Danh sách các khu vực có sẵn:")
for idx, location in enumerate(available_locations, start=1):
    print(f"{idx}. {location}")

# Lựa chọn khu vực từ bàn phím
while True:
    choice = input("Chọn khu vực (nhập số 1, 2, ... hoặc Enter để thoát): ")

    if not choice:
        print("Thoát chương trình.")
        break

    if is_number(choice):
        choice = int(choice)
        if 1 <= choice <= len(available_locations):
            location = available_locations[choice - 1]
            result_df = calculate(location)
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")








