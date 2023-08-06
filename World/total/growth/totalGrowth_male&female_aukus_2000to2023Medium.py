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
        "Time": {"$gte": 2000, "$lte": 2023}
    }))

    df = pd.DataFrame(data)

    # Tính tổng dân số đã tăng của "popmale" và "popfemale" trong khu vực AUKUS từ 1950 đến 2000
    total_popmale_growth = df['PopMale'].iloc[-1] - df['PopMale'].iloc[0]
    total_popfemale_growth = df['PopFemale'].iloc[-1] - df['PopFemale'].iloc[0]

    # Tính phần trăm tăng trưởng dân số của "popmale" và "popfemale"
    popmale_growth_percent = (total_popmale_growth / df['PopMale'].iloc[0]) * 100
    popfemale_growth_percent = (total_popfemale_growth / df['PopFemale'].iloc[0]) * 100

    # Xuất kết quả tổng dân số đã tăng và phần trăm tăng trưởng qua console log
    print(f"Tổng dân số đã tăng và phần trăm tăng trưởng của khu vực {location} (Variant: Medium) từ 2000 đến 2023:")
    print(f"Tổng dân số đã tăng PopMale: {total_popmale_growth}")
    print(f"Phần trăm tăng trưởng PopMale: {popmale_growth_percent:.2f}%")
    print(f"Tổng dân số đã tăng PopFemale: {total_popfemale_growth}")
    print(f"Phần trăm tăng trưởng PopFemale: {popfemale_growth_percent:.2f}%")

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











