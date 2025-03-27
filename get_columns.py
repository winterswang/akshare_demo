import pandas as pd
import os

def get_csv_columns(csv_file):
    """读取CSV文件并获取列名"""
    try:
        df = pd.read_csv(csv_file)
        return df.columns.tolist()
    except Exception as e:
        print(f"读取文件 {csv_file} 时发生错误：{str(e)}")
        return []

def save_columns_to_txt(columns, output_file):
    """将列名保存到txt文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for column in columns:
                f.write(f"{column}\n")
        print(f"已成功保存列名到文件：{output_file}")
    except Exception as e:
        print(f"保存文件 {output_file} 时发生错误：{str(e)}")

def main():
    # 获取A股和港股的示例股票代码
    a_stock_code = '000001'
    hk_stock_code = '00001'
    
    # 定义文件映射关系
    file_mappings = {
        # A股文件映射
        f'{a_stock_code}_balance_sheet.csv': 'balance_columns.txt',
        f'{a_stock_code}_cash_flow.csv': 'cash_flow_columns.txt',
        f'{a_stock_code}_financial_indicator.csv': 'financial_columns.txt',
        f'{a_stock_code}_income_statement.csv': 'income_columns.txt',
        # 港股文件映射
        f'{hk_stock_code}_hk_balance_sheet.csv': 'hk_balance_columns.txt',
        f'{hk_stock_code}_hk_cash_flow.csv': 'hk_cash_flow_columns.txt',
        f'{hk_stock_code}_hk_financial_indicator.csv': 'hk_financial_columns.txt',
        f'{hk_stock_code}_hk_income_statement.csv': 'hk_income_columns.txt'
    }
    
    # 遍历处理每个文件
    for csv_file, txt_file in file_mappings.items():
        csv_path = os.path.join('finance', csv_file)
        txt_path = os.path.join('finance', txt_file)
        
        # 获取列名并保存
        if os.path.exists(csv_path):
            columns = get_csv_columns(csv_path)
            if columns:
                save_columns_to_txt(columns, txt_path)
        else:
            print(f"文件不存在：{csv_path}")

if __name__ == '__main__':
    main()