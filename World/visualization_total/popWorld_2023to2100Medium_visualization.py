import pymongo
import pandas as pd
import matplotlib.pyplot as plt

# Kết nối tới MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Tạo hoặc chọn cơ sở dữ liệu
mydb = myclient["2174802010439"]

# Tạo hoặc chọn bảng (collection) để lưu trữ dữ liệu
collection = mydb["population"]

# Truy vấn để lấy danh sách các kịch bản "Variant" có sẵn trong dữ liệu
available_variants = collection.distinct("Variant")

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', None)

# In danh sách các kịch bản "Variant" cho người dùng lựa chọn
print("Danh sách các kịch bản (Variant) có sẵn:")
for idx, variant in enumerate(available_variants, start=1):
    print(f"{idx}. {variant}")

# Yêu cầu người dùng nhập vào kịch bản "Variant" và các năm
while True:
    variant_choice = input("Nhập số tương ứng với kịch bản (hoặc Enter để thoát): ")

    if not variant_choice:
        print("Thoát chương trình.")
        break

    if variant_choice.isdigit():
        variant_choice = int(variant_choice)
        if 1 <= variant_choice <= len(available_variants):
            selected_variant = available_variants[variant_choice - 1]

            # Yêu cầu nhập năm từ người dùng
            year_start = int(input("Nhập năm bắt đầu: "))
            year_end = int(input("Nhập năm kết thúc: "))

            # Truy vấn để lấy các bản ghi có kịch bản (variant) và các năm trong danh sách năm cho trước
            query = {
                "Variant": selected_variant,
                "Time": {"$in": list(range(year_start, year_end + 1))}
            }

            # Lấy dữ liệu từ MongoDB và đưa vào DataFrame
            data = list(collection.find(query, {"_id": 0}))
            df = pd.DataFrame(data)

            # Tính tổng dân số "PopMale" và "PopFemale" của tất cả khu vực "Location" cho các năm trong danh sách năm
            total_popmale = df.groupby("Time")["PopMale"].sum()
            total_popfemale = df.groupby("Time")["PopFemale"].sum()

            # Tính số lượng và phần trăm đã tăng lên giữa các năm trong danh sách năm
            popmale_growth_percent = ((total_popmale - total_popmale.iloc[0]) / total_popmale.iloc[0]) * 100
            popfemale_growth_percent = ((total_popfemale - total_popfemale.iloc[0]) / total_popfemale.iloc[0]) * 100

            # In kết quả tổng dân số và phần trăm tăng trưởng qua console log
            print(f"Kịch bản (Variant): {selected_variant}")
            print(f"Phần trăm tăng trưởng 'PopMale' từ năm {year_start} đến {year_end}:")
            print(popmale_growth_percent)
            print(f"Phần trăm tăng trưởng 'PopFemale' từ năm {year_start} đến {year_end}:")
            print(popfemale_growth_percent)

            # Trực quan hóa dữ liệu với biểu đồ cột
            years_range = list(range(year_start, year_end + 1))
            plt.bar(years_range, popmale_growth_percent, color='blue', label='PopMale')
            plt.bar(years_range, popfemale_growth_percent, color='orange', label='PopFemale', bottom=popmale_growth_percent)
            plt.xlabel("Năm")
            plt.ylabel("Phần trăm tăng trưởng")
            plt.title(f"Tăng trưởng dân số cho '{selected_variant}' từ {year_start} đến {year_end}")
            plt.legend()
            plt.show()

        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
    else:
        print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
