import pandas as pd
import numpy as np
from pymongo import MongoClient

def export_excel(export):
    # 将字典列表转换为DataFrame
    df = pd.DataFrame(list(export))
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter('carhome.xlsx')
    # 替换空单元格
    df.fillna(np.nan, inplace=True)
    # 输出
    df.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()


if __name__ == '__main__':
    # 将MongoDB数据转成xlsx文件
    client = MongoClient()
    connection = client['test']['car_home']
    ret = connection.find({}, {'_id': 0})
    data_list = list(ret)
    export_excel(data_list)