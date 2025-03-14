import yaml
import akshare as ak
import os
from datetime import datetime

def load_config(config_file):
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def download_a_stock_finance(code, save_dir):
    """下载A股财务数据"""
    # 转换股票代码格式
    if code.startswith('6'):
        symbol = f'SH{code}'
    else:
        symbol = f'SZ{code}'
    
    # 下载三大报表数据
    try:
        # 资产负债表
        balance_sheet = ak.stock_balance_sheet_by_report_em(symbol=symbol)
        balance_sheet.to_csv(f'{save_dir}/{code}_balance_sheet.csv', encoding='utf-8-sig')
        
        # 利润表
        income_statement = ak.stock_profit_sheet_by_report_em(symbol=symbol)
        income_statement.to_csv(f'{save_dir}/{code}_income_statement.csv', encoding='utf-8-sig')
        
        # 现金流量表
        cash_flow = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)
        cash_flow.to_csv(f'{save_dir}/{code}_cash_flow.csv', encoding='utf-8-sig')
        
        # 财务分析指标
        financial_analysis = ak.stock_financial_analysis_indicator(symbol=code, start_year="2020")
        financial_analysis.to_csv(f'{save_dir}/{code}_financial_analysis.csv', encoding='utf-8-sig')
        
        print(f'成功下载A股 {code} 的财务数据')
    except Exception as e:
        print(f'下载A股 {code} 的财务数据失败: {str(e)}')

def download_hk_stock_finance(code, save_dir):
    """下载港股财务数据"""
    try:
        # 资产负债表
        balance_sheet = ak.stock_financial_hk_report_em(stock=code, symbol='资产负债表', indicator='年度')
        balance_sheet.to_csv(f'{save_dir}/{code}_balance_sheet.csv', encoding='utf-8-sig')
        
        # 利润表
        income_statement = ak.stock_financial_hk_report_em(stock=code, symbol='利润表', indicator='年度')
        income_statement.to_csv(f'{save_dir}/{code}_income_statement.csv', encoding='utf-8-sig')
        
        # 现金流量表
        cash_flow = ak.stock_financial_hk_report_em(stock=code, symbol='现金流量表', indicator='年度')
        cash_flow.to_csv(f'{save_dir}/{code}_cash_flow.csv', encoding='utf-8-sig')
        
        # 财务分析指标
        financial_analysis = ak.stock_financial_hk_analysis_indicator_em(symbol=code, indicator="年度")
        financial_analysis.to_csv(f'{save_dir}/{code}_financial_analysis.csv', encoding='utf-8-sig')
        
        print(f'成功下载港股 {code} 的财务数据')
    except Exception as e:
        print(f'下载港股 {code} 的财务数据失败: {str(e)}')

def download_us_stock_finance(code, save_dir):
    """下载美股财务数据"""
    try:
        # 资产负债表
        balance_sheet = ak.stock_financial_us_report_em(stock=code, symbol='资产负债表', indicator='年报')
        balance_sheet.to_csv(f'{save_dir}/{code}_balance_sheet.csv', encoding='utf-8-sig')
        
        # 利润表
        income_statement = ak.stock_financial_us_report_em(stock=code, symbol='综合损益表', indicator='年报')
        income_statement.to_csv(f'{save_dir}/{code}_income_statement.csv', encoding='utf-8-sig')
        
        # 现金流量表
        cash_flow = ak.stock_financial_us_report_em(stock=code, symbol='现金流量表', indicator='年报')
        cash_flow.to_csv(f'{save_dir}/{code}_cash_flow.csv', encoding='utf-8-sig')
        
        # 财务分析指标
        financial_analysis = ak.stock_financial_us_analysis_indicator_em(symbol=code, indicator="年报")
        financial_analysis.to_csv(f'{save_dir}/{code}_financial_analysis.csv', encoding='utf-8-sig')
        
        print(f'成功下载美股 {code} 的财务数据')
    except Exception as e:
        print(f'下载美股 {code} 的财务数据失败: {str(e)}')

def main():
    # 创建保存财务数据的目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    finance_dir = os.path.join(base_dir, 'finance_data')
    os.makedirs(finance_dir, exist_ok=True)
    
    # 加载配置文件
    config = load_config(os.path.join(base_dir, 'config.yaml'))
    
    # 遍历股票列表下载数据
    for stock in config['stocks']:
        code = stock['code']
        market_type = stock['market_type']
        
        # 创建股票专属目录
        stock_dir = os.path.join(finance_dir, f'{market_type}_{code}')
        os.makedirs(stock_dir, exist_ok=True)
        
        # 根据市场类型调用对应的下载函数
        if market_type == 'A':
            download_a_stock_finance(code, stock_dir)
        elif market_type == 'HK':
            download_hk_stock_finance(code, stock_dir)
        elif market_type == 'US':
            download_us_stock_finance(code, stock_dir)

if __name__ == '__main__':
    main()