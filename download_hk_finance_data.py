import akshare as ak
import sqlite3
import pandas as pd
import os
from column_mapping import load_mapping_file, map_columns, process_hk_numeric_columns

# 创建finance文件夹（如果不存在）
if not os.path.exists('finance'):
    os.makedirs('finance')

# 从数据库读取第一条港股数据
def get_first_stock():
    conn = sqlite3.connect('db/h_stock.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock_code FROM h_stock_realtime LIMIT 1')
    stock = cursor.fetchone()
    conn.close()
    return stock

def download_financial_data(stock_code):
    # 港股代码格式处理（补齐5位）
    stock_code = stock_code.zfill(5)
    
    # 加载映射文件
    finance_mapping = load_mapping_file('api_txt/format/h_finance_mapping.txt')
    
    try:
        # 下载资产负债表
        balance_sheet = ak.stock_financial_hk_report_em(stock=stock_code, symbol="资产负债表", indicator="年度")
        
        # 验证数据列是否存在
        required_columns = ['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_NAME', 'STD_ITEM_CODE', 'REPORT_DATE', 'AMOUNT']
        if not all(col in balance_sheet.columns for col in required_columns):
            raise ValueError(f"资产负债表数据缺少必要列，现有列: {balance_sheet.columns.tolist()}")

        # 转换并保存资产负债表
        balance_sheet = balance_sheet.pivot(
            index=['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME'],
            columns='REPORT_DATE',
            values='AMOUNT'
        ).reset_index()
        date_columns = sorted([col for col in balance_sheet.columns if col not in ['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME']], reverse=True)
        balance_sheet = balance_sheet[['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME'] + date_columns]
        balance_sheet = balance_sheet.sort_values('STD_ITEM_CODE')
        balance_sheet.to_csv(f'finance/{stock_code}_hk_balance_sheet.csv', index=False, encoding='utf-8')
        
        # 下载并转换现金流量表
        cash_flow = ak.stock_financial_hk_report_em(stock=stock_code, symbol="现金流量表", indicator="年度")
        
        # 验证数据列是否存在
        if not all(col in cash_flow.columns for col in required_columns):
            raise ValueError(f"现金流量表数据缺少必要列，现有列: {cash_flow.columns.tolist()}")
            
        cash_flow = cash_flow.pivot(
            index=['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME'],
            columns='REPORT_DATE',
            values='AMOUNT'
        ).reset_index()
        date_columns = sorted([col for col in cash_flow.columns if col not in ['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME']], reverse=True)
        cash_flow = cash_flow[['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME'] + date_columns]
        cash_flow = cash_flow.sort_values('STD_ITEM_CODE')
        cash_flow.to_csv(f'finance/{stock_code}_hk_cash_flow.csv', index=False, encoding='utf-8')
        
        # 下载并转换利润表
        income_statement = ak.stock_financial_hk_report_em(stock=stock_code, symbol="利润表", indicator="年度")
        
        # 验证数据列是否存在
        if not all(col in income_statement.columns for col in required_columns):
            raise ValueError(f"利润表数据缺少必要列，现有列: {income_statement.columns.tolist()}")
            
        income_statement = income_statement.pivot(
            index=['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME'],
            columns='REPORT_DATE',
            values='AMOUNT'
        ).reset_index()
        date_columns = sorted([col for col in income_statement.columns if col not in ['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME']], reverse=True)
        income_statement = income_statement[['SECUCODE', 'SECURITY_NAME_ABBR', 'STD_ITEM_CODE', 'STD_ITEM_NAME'] + date_columns]
        income_statement = income_statement.sort_values('STD_ITEM_CODE')
        income_statement.to_csv(f'finance/{stock_code}_hk_income_statement.csv', index=False, encoding='utf-8')
        
        # 下载财务指标
        financial_indicator = ak.stock_financial_hk_analysis_indicator_em(symbol=stock_code)
        financial_indicator = map_columns(financial_indicator, finance_mapping)
        financial_indicator = process_hk_numeric_columns(financial_indicator)
        financial_indicator.to_csv(f'finance/{stock_code}_hk_financial_indicator.csv', index=False, encoding='utf-8')
        
        print(f"成功下载并保存{stock_code}的港股财务报表数据")
        
    except Exception as e:
        print(f"下载{stock_code}的港股财务报表数据时出错: {str(e)}")

def main():
    # 获取第一条港股数据
    stock = get_first_stock()
    if stock:
        stock_code = stock[0]  # stock_code是第一个字段
        download_financial_data(stock_code)
    else:
        print("未能从数据库获取港股数据")

if __name__ == '__main__':
    main()