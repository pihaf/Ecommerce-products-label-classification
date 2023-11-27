# import urllib.parse
# import json

# input_file = "missing_labels2.txt"
# base_url = "https://vatgia.com/home/"
# sitemap = {"_id": "vatgia", "startUrl": []}

# # Read items from input file
# with open(input_file, "r", encoding='utf-8') as file:
#     items = file.read().splitlines()

# startURL = []
# for item in items:
#     # encoded_item = urllib.parse.quote(item.lower().replace(" ", "%2c"))
#     temp = item.lower().replace(" ", "+")
#     # Encode the modified item for URL
#     encoded_item = urllib.parse.quote(temp)
#     url = base_url + encoded_item + ".spvg"
#     sitemap["startUrl"].append(url)

# output_file = "sitemap2.json"
# # # Save sitemap to JSON file
# # with open(output_file, "w", encoding='utf-8') as file:
# #     for item in startURL:
# #         file.write('"'+ item + '",')
# # Save sitemap to JSON file
# with open(output_file, "w", encoding='utf-8') as file:
#     json.dump(sitemap, file)

# print(f"Sitemap JSON saved to {output_file}")

# '''{"_id":"vatgia","startUrl":[]}'''

# import pandas as pd

# data = pd.read_csv('new.csv')
# columns = ['link2', 'title2']
# new = data[columns]
# new.to_csv('new2.csv', index=False)

# import urllib.parse
# import pandas as pd

# # Read the CSV file
# df = pd.read_csv('missing2.csv')

# # Function to remove the specified part from the URL
# def remove_part(url):
#     return url.replace('https://vatgia.com/home/', '')

# # Function to decode URL-encoded string to UTF-8 and capitalize the first letter
# def decode_and_capitalize(url):
#     utf8_string = urllib.parse.unquote(url, encoding='utf-8')
#     result = utf8_string.replace('+', ' ')
#     result = result.capitalize()
#     return result

# def remove_tail(url):
#     return url.replace('.spvg', '')

# # Remove the specified part from the URLs in the first column
# df['start-url'] = df['start-url'].apply(remove_part)

# # Replace URLs in the first column with the decoded and capitalized strings
# df['start-url'] = df['start-url'].apply(decode_and_capitalize)

# df['start-url'] = df['start-url'].apply(remove_tail)

# df.to_csv('final_missing2.csv', index=False)

# import pandas as pd

# # Read the text file
# with open('product_test_unlabeled.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()

# # Remove newline characters and create a list of labels
# labels = [line.strip() for line in lines]

# # Create a dataframe with 'Label' column
# df = pd.DataFrame({'Label': labels})

# # Save the dataframe to a CSV file
# df.to_csv('output.csv', index=False)

import pandas as pd

# Read the dataframe from a file or create it
df = pd.read_csv('predicted_labels2.csv')
lastpart = pd.read_csv('lastpart.csv')
df2 = pd.read_csv('additionals.csv')

# Specify the product and the string to replace the label
substring_to_match = 'Máy phát điện'# Bảng
substring_to_match2 = 'Động cơ'# Shinwa
replacement_label = 'Máy phát điện công nghiệp'

substring_replacements = {
    'Thắt lưng nam': 'Dây lưng (thắt lưng) nam',
    'Thắt lưng nữ': 'Dây lưng (thắt lưng) nữ',
    'Cưa tay': 'Cưa tay',
    'Cưa gỗ':'Cưa tay',
    'Đèn tường': 'Đèn tường',
    'Máy mài góc': 'Máy mài góc',
    'Caravat nam': 'Caravat nam',
    'Sập thờ': 'Sập thờ',
    'Drum': 'Linh kiện máy in',
    'Máy Cắt Gạch': 'Máy cắt đá',
    'Tam giác phản quang ': 'Biển báo giao thông',
    'Kem lót': 'Kem lót',
    'Vali': 'Vali, Hành lý',
    'Cặp học sinh': 'Cặp học sinh',
    'Đồng hồ nữ Skmei': 'Đồng hồ hàng hiệu nữ',
    'Đồ ngủ thun lạnh': 'Đồ ngủ nữ',
    'Máy rút màng': 'Máy rút màng co ( máy hút màng co )',
    'Máy đo độ đồng tâm' : 'Dụng cụ đo, kiểm tra khác',
    'Máy đo độ ẩm': 'Thiết bị đo độ ẩm',
    'Xe bán hàng': 'Quầy xe lưu động ( quầy bán hàng di động )',
    'Đồng hồ đôi': 'Đồng hồ đôi',
    'Sữa rửa mặt': 'Sữa rửa mặt',
    'Mũi khoan': 'Mũi khoan',
    'Tủ sắt quần áo': 'Tủ quần áo',
    'MÁY KHOAN': 'Máy khoan cầm tay',
    'Thiết bị đo nhiệt độ': 'Thiết bị đo nhiệt độ',
    'Biến tần':'Biến tần',
    'Thiết kế quảng cáo': 'Thiết kế quảng cáo',
    'RAM': 'RAM (Server)',
    'Bóp nam': 'Ví, bóp nam',
    'Ví nam': 'Ví, bóp nam',
    'Giường gỗ': 'Giường',
    'Bàn thờ thần tài': 'Tủ thờ Thần Tài',
    'Bàn thờ treo': 'Bàn thờ treo',
    'Bàn thờ ông địa': 'Tủ thờ Thần Tài',
    'Bếp Gas Dương Mặt Kính': 'Bếp gas',
    'Ốp': 'Bao đựng, ốp lưng điện thoại',
    'Kem đánh răng': 'Kem đánh răng',
    'Đèn vách': 'Đèn vách',
    'Gạch bông': 'Gạch bông',
    'Mặt Nạ': 'Mặt nạ',
    'Túi ngủ': 'Đồ dùng sinh hoạt khác',
    'Đàn Piano điện': 'Đàn Piano điện (Digital Pianos)',
    'Cửa thép chống cháy': 'Cửa chống cháy',
    'Xe Đẩy Thức Ăn': 'Xe đẩy, giá thức ăn',
    'Tẩu đuôi chuột': 'Cờ lê',
    'Nước hoa nam': 'Nước hoa nam',
    'Nước Hoa Nam': 'Nước hoa nam',
    'Nước hoa nữ': 'Nước hoa nữ',
    'Nước Hoa Nữ': 'Nước hoa nữ',
    'Thau nhựa': 'Xô, thùng, chậu nhựa',
    'Bàn chải đánh răng': 'Bàn chải đánh răng',
    'Dây đèn LED': 'Bộ đèn trang trí',
    'Máy thái thịt': 'Máy thái lát thịt',
    'Cầu Dao Tự Động': 'Cầu dao tự động ( Aptomat )',
    'Cầu dao đóng ngắt': 'Cầu dao tự động ( Aptomat )',
    'Tam cấp khảm ốc': 'Đồ thờ khác',
    'Đồng phục mẫu giáo': 'Đồng phục mẫu giáo',
    'Đồng phục mầm non': 'Đồng phục mẫu giáo',
    'Sữa bột' : 'Sữa bột',
    'Quạt làm mát biến tần': 'Phụ kiện tủ điện',
    'Xe gom rác': 'Xe đẩy',
    'Chân máy ảnh': 'Chân máy ảnh (Tripod)',
    'Kẹo Nổ Striking': 'Kẹo hoa quả',
    'Bộ nước hoa mini': 'Nước hoa nữ',
    'Bulong':'Bu lông, tắc kê',
    'Lưới rào': 'Lưới thép',
    'Lưới an toàn': 'Lưới an toàn',
    'Lưới cẩu hàng': 'Lưới địa kỹ thuật, lưới xây dựng',
    'Biến thế hàn': 'Máy biến áp',
    'Nước hoa pha lê': 'Nước hoa ôtô',
    'Đồng phục lớp': 'Đồng phục học sinh- sinh viên',
    'Nệm gòn': 'Đệm (Nệm)',
    'Tủ Lạnh Công Nghiệp': 'Tủ lạnh công nghiệp',
    'Kính Mắt': 'Mắt kính thời trang',
    'Kim Thu Sét': 'Thiết bị phòng chống sét',
    'Kim thu sét': 'Thiết bị phòng chống sét',
    'Thiết kế thi công': 'Thi công xây dựng',
    'Thiết kế quảng cáo': 'Thiết kế quảng cáo',
    'Thiết kế phòng khách': 'Thiết kế phòng khách',
    'Thiết kế phòng ngủ': 'Thiết kế nội thất khác',
    'Thiết kế phòng bếp': 'Thiết kế nội thất khác',
    'Thiết kế phòng nhân viên': 'Thiết kế nội thất khác',
    'Đèn chùm pha lê': 'Đèn chùm',
    'Nhẫn nam': 'Nhẫn nam',
    'Nhẫn nữ': 'Nhẫn nữ',
    'Nhẫn đôi': 'Nhẫn cưới, nhẫn đính hôn',
    'Nhẫn vương miện': 'Nhẫn nữ',
    'Nhẫn tay': 'Nhẫn nữ',
    'ảo thuật': 'Đạo cụ ảo thuật',
    'Đồng Hồ Cặp Đôi': 'Đồng hồ đôi',
    'Đèn chùm': 'Đèn chùm', 
    'Đèn Chùm': 'Đèn chùm', 
    'Đèn thả': 'Đèn thả',
    'Đèn pha lê': 'Đèn pha lê',
    'Đèn ngủ': 'Đèn ngủ',
    'Đèn led đường phố ': 'Đèn chiếu sáng công cộng',
    'Lương khô': 'Thực phẩm khô khác',
    'Sạc pin laptop': 'Sạc pin laptop (Adapter)',
    'Sạc pin máy quay': 'Sạc pin máy ảnh, máy quay',
    'Sạc pin máy ảnh': 'Sạc pin máy ảnh, máy quay',
    'Tăng phô': 'Chấn lưu',
    'Ghế cắt tóc': 'Ghế cắt tóc',
    'Máy ép dầu ly tâm Kusami': 'Máy ép dầu đậu nành',
    'Máy seal màng nhôm': 'Máy ép màng nhôm',
    'Máy Ly Tâm': 'Máy li tâm',
    'Khuôn': 'Khuôn mẫu các loại',
    'MÁY VẮT SỔ': 'Máy vắt sổ',
    'Máy vắt sổ':'Máy vắt sổ',
    'Kính lọc vuông':'Kính lọc (Filter)',
    'Máy uốn ống': 'Máy uốn ống thường',
    'Dép nhựa nam quai ngang': 'Dép, Sandal nam',
    'Máy hâm sữa': 'Máy tiệt trùng - Hâm sữa',
    'Máy Phân Tích Máu': 'Máy xét nghiệm máu',
    'Máy sấy khí': 'Máy sấy khí nén',
    'Máy sấy tóc': 'Máy sấy tóc',
    'Máy thùa khuy': 'Máy thùa khuy',
    'Máy xông hơi ướt': 'Máy xông hơi ướt',
    'bột giặt': 'Bột giặt',
    'Viên giặt': 'Bột giặt',
    'Nước giặt': 'Bột giặt',
    'Pa lăng': 'Pa Lăng',
    'Pa Lăng': 'Pa Lăng',
    'Bộ đồ ngủ': 'Đồ ngủ nữ',
    'Ủng': 'Giầy, ủng bảo hộ',
    'Xịt khoáng':'Sản phẩm dưỡng da mặt',
    'Xịt Khoáng': 'Sản phẩm dưỡng da mặt',
    'Hộp Tỳ Tay':'Hộp tỳ tay trên Ô tô',
    'Tủ nấu cơm bằng điện': 'Tủ nấu cơm công nghiệp',
    'Bẫy mỡ': 'Phụ kiện nhà bếp công nghiệp',
    'Cảm biến nhiệt độ': 'Cảm biến nhiệt độ',
    'Bộ điều khiển nhiệt độ': 'Bộ điều khiển nhiệt độ',
    'Máy khuếch tán , phun sương': 'Máy phun sương tăng độ ẩm',
    'Máy xay cà phê': 'Máy xay cà phê',
    'Máy lọc nước':'Máy lọc nước',
    'Máy chà sàn': 'Máy chà sàn',
    'Máy Chà Sàn': 'Máy chà sàn',
    'Máy làm đá': 'Máy làm đá siêu tốc',
    'Máy Làm Đá': 'Máy làm đá siêu tốc',
    'Máy hút mùi':'Máy hút mùi',
    'Máy Hút Mùi':'Máy hút mùi',
    'Hút mùi':'Máy hút mùi',
    'Máy Bơm Dầu Nhớt Khí Nén': 'Máy bơm hút dầu, mỡ',
    'Máy bơm mỡ': 'Máy bơm hút dầu, mỡ',
    'Máy lọc nước': 'Máy lọc nước',
    'MÁY KHOAN VẶN VÍT': 'Máy khoan cầm tay',
    'Máy khoan và vặn vít': 'Máy khoan cầm tay',
    'Máy khoan cầm tay': 'Máy khoan cầm tay',
    'Máy khoan vặn vít': 'Máy khoan cầm tay',
    'Pallet nhựa': 'Pallet',
    'Pallet sắt': 'Pallet',
    'Pallet inox': 'Pallet',
    'Pallet liền khối': 'Pallet',
    'Pallet gỗ': 'Pallet',
    'Đầu mũi': 'Phụ kiện dụng cụ sửa chữa',
    'Gương cầu lồi xoay 360 độ': 'Gương, kính ô tô',
    'Bodysuit': 'Body liền cho bé',
    'Thước xếp': 'Thước xếp',
    'Thước Xếp': 'Thước xếp',
    'Thước Thủy': 'Thước thuỷ',
    'Thước thẳng': 'Thước thẳng'
}

validation = pd.read_csv('validation_data.csv')

result_dict = {}
for index, row in validation.iterrows():
    value = row['Label']
    result_dict[value] = value

save = ['Tủ lạnh', 'Máy sủi', 'Lương khô']

# Iterate over the substrings and replacement labels, and update the 'Label' values
for substring, replacement_label in substring_replacements.items():
    df2.loc[df2['Product Name'].str.contains(substring), 'Label'] = replacement_label

# for substring, replacement_label in substring_replacements.items():
#     lastpart.loc[lastpart['Product Name'].str.contains(substring), 'Label'] = replacement_label

# Replace the label for the specific product
#df.loc[df['Product Name'].str.contains(substring_to_match) & df['Product Name'].str.contains(substring_to_match2), 'Label'] = replacement_label
#df.loc[df['Product Name'].str.startswith(substring_to_match), 'Label'] = replacement_label

# Save the updated dataframe back to the CSV file
#df.to_csv('predicted_labels2.csv', index=False)
# lastpart.to_csv('lastpart.csv', index=False)
df2.to_csv('additionals.csv', index=False)

# for substring, replacement_label in result_dict.items():
#     lastpart.loc[lastpart['Product Name'].str.contains(substring), 'Label'] = replacement_label
print("Done")