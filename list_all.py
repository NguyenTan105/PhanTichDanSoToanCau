import pymongo

# Kết nối tới MongoDB
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Tạo hoặc chọn cơ sở dữ liệu
mydb = myclient["2174802010439"]

# Tạo hoặc chọn bảng (collection) để lưu trữ dữ liệu
collection = mydb["population"]

# Hàm thực hiện truy vấn sản phẩm và hiển thị kết quả
def list_all_products():
    all_products = collection.find({})

    print("\nKết quả truy vấn:")
    for item in all_products:
        locID = int(item['LocID'])
        sdmxCode = int(item['SDMX_code'])
        locTypeID = int(item['LocTypeID'])
        locTypeID = int(item['LocTypeID'])
        varID = int(item['VarID'])
        # SortOrder,
        # LocID,Notes,
        # ISO3_code,
        # ISO2_code,SDMX_code,
        # LocTypeID,
        # LocTypeName,
        # ParentID,
        # Location,
        # VarID,
        # Variant,
        # Time,
        # MidPeriod,
        ''' #! (milion people)
        PopMale,
        PopFemale,
        PopTotal,
        '''
        # PopDensity #!(person/km2)
        
        print(f"SortOrder: {item}, LocID: {item['LocID']}, Notes: {item['Notes']}, ISO3_code: {item['ISO3_code']}, ISO2_code: {item['ISO2_code']}, SDMX_code: {item['SDMX_code']}, LocTypeID: {item['LocTypeID']}, LocTypeName: {item['LocTypeName']}, Location: {item['Location']},VarID: {item['VarID']}, Variant: {item['Variant']}, Time: {item['Time']}, MidPeriod: {item['MidPeriod']}, PopMale: {item['PopMale']}, PopFemale: {item['PopFemale']}, PopTotal: {item['PopTotal']}, PopDensity: {item['PopDensity']},")

list_all_products()