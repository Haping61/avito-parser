import os
import csv
import time
import pandas as pd

def write_data(data):
    local_time = time.localtime()
    format_local_time = time.strftime("%D-%H:%M:%S", local_time)
    format_local_time = format_local_time.replace('/', '.')
    
    with open('data.csv', 'w', newline='', encoding='utf-8') as table:
        table_writer = csv.writer(table, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        table_writer.writerow(['Title', 'Price', 'Description', 'Link'])
        for item in data[::-1]:
            table_writer.writerow(item)
    csv_file = pd.read_csv('./data.csv')
    csv_file.to_excel(f'./{format_local_time}.xlsx')
    os.remove('./data.csv')
