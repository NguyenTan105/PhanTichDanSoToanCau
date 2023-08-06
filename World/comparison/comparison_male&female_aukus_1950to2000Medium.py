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

# Hàm tính số lượng và phần trăm "popmale" ít hơn bao nhiêu so với "popfemale" qua các năm từ 1950 đến 2000
def calculate_popmale_vs_popfemale(location):
    # Lấy dữ liệu từ MongoDB theo yêu cầu (khu vực, variant "medium", năm từ 1950 đến 2000)
    data = list(collection.find({
        "Location": location,
        "Variant": "Medium",
        "Time": {"$gte": 1950, "$lte": 2000}
    }))

    df = pd.DataFrame(data)

    # Tính số lượng và phần trăm "popmale" ít hơn bao nhiêu so với "popfemale" qua các năm
    df['PopMale_VS_PopFemale'] = df['PopFemale'] - df['PopMale']
    df['PopMale_Percentage_VS_PopFemale'] = (df['PopMale_VS_PopFemale'] / df['PopFemale']) * 100

    return df[['Time', 'PopMale_VS_PopFemale', 'PopMale_Percentage_VS_PopFemale']]

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
            result_df = calculate_popmale_vs_popfemale(location)
            print(result_df)
            print(f"Đây là số lượng và phần trăm 'popmale' so với 'popfemale' tại khu vực {location} (Variant: Medium) từ 1950 đến 2000")
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
