import pymongo
import pandas as pd
import matplotlib.pyplot as plt
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
        "Time": {"$gte": 1950, "$lte": 2023}
    }))

    df = pd.DataFrame(data)

    # Tổng hợp dữ liệu dân số theo năm và giới tính cho kịch bản "Medium"
    df_population = df.groupby(['Time'])[['PopMale', 'PopFemale']].sum().reset_index()

    # Trực quan hóa dữ liệu bằng matplotlib - Biểu đồ đường (line chart)
    plt.figure(figsize=(10, 6))

    plt.plot(df_population['Time'], df_population['PopMale'], label='Dân số nam (Medium)')
    plt.plot(df_population['Time'], df_population['PopFemale'], label='Dân số nữ (Medium)')

    plt.xlabel("Năm")
    plt.ylabel("Tổng dân số")
    plt.title(f"Biểu đồ quá trình gia tăng dân số giữa PopMale và PopFemale của khu vực {location} (Medium) (1950-2023)")
    plt.legend()
    plt.xticks(rotation=45)  # Xoay năm để tránh trùng nhau
    plt.tight_layout()  # Cân chỉnh kích thước biểu đồ để hiển thị đầy đủ
    plt.show()

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






