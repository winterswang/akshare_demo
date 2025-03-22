import akshare as ak
import sqlite3
import pandas as pd
import os
from column_mapping import load_mapping_file, map_columns, process_numeric_columns

# 创建finance文件夹（如果不存在）
if not os.path.exists('finance'):
    os.makedirs('finance')

# 从数据库读取第一条股票数据
def get_first_stock():
    conn = sqlite3.connect('db/a_stock.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock_code FROM a_stock_realtime LIMIT 1')
    stock = cursor.fetchone()
    conn.close()
    return stock

def download_financial_data(stock_code):
    # 转换股票代码格式
    symbol = f"SH{stock_code}" if stock_code.startswith('6') else f"SZ{stock_code}"
    
    # 加载映射文件
    balance_mapping = load_mapping_file('api_txt/format/balance_mapping.txt')
    cash_mapping = load_mapping_file('api_txt/format/cash_mapping.txt')
    income_mapping = load_mapping_file('api_txt/format/income_mapping.txt')
    
    try:
        # 下载资产负债表
        balance_sheet = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        balance_sheet = map_columns(balance_sheet, balance_mapping)
        balance_sheet = process_numeric_columns(balance_sheet)
        balance_sheet.to_csv(f'finance/{stock_code}_balance_sheet.csv', index=False, encoding='utf-8')
        
        # 下载现金流量表
        cash_flow = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        cash_flow = map_columns(cash_flow, cash_mapping)
        cash_flow = process_numeric_columns(cash_flow)
        cash_flow.to_csv(f'finance/{stock_code}_cash_flow.csv', index=False, encoding='utf-8')
        
        # 下载利润表
        income_statement = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        income_statement = map_columns(income_statement, income_mapping)
        income_statement = process_numeric_columns(income_statement)
        income_statement.to_csv(f'finance/{stock_code}_income_statement.csv', index=False, encoding='utf-8')
        
        # 下载财务指标
        financial_indicator = ak.stock_financial_analysis_indicator(symbol=stock_code, start_year = '2010')
        financial_indicator.to_csv(f'finance/{stock_code}_financial_indicator.csv', index=False, encoding='utf-8')
        
        print(f"成功下载并保存{stock_code}的财务报表数据")
        
    except Exception as e:
        print(f"下载{stock_code}的财务报表数据时出错: {str(e)}")

def main():
    # 获取第一条股票数据
    stock = get_first_stock()
    if stock:
        stock_code = stock[0]  # stock_code是第一个字段
        download_financial_data(stock_code)
    else:
        print("未能从数据库获取股票数据")

if __name__ == '__main__':
    main()