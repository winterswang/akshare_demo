import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import numpy as np
from matplotlib.gridspec import GridSpec

# 设置中文字体
try:
    # 尝试使用系统中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'Heiti TC', 'WenQuanYi Micro Hei']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
except:
    print("警告：可能无法正确显示中文")

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# 财务数据文件路径
FINANCIAL_INDICATOR_PATH = os.path.join(ROOT_DIR, 'finance', '000001_financial_indicator.csv')
BALANCE_SHEET_PATH = os.path.join(ROOT_DIR, 'finance', '000001_balance_sheet.csv')
INCOME_STATEMENT_PATH = os.path.join(ROOT_DIR, 'finance', '000001_income_statement.csv')
CASH_FLOW_PATH = os.path.join(ROOT_DIR, 'finance', '000001_cash_flow.csv')

# 输出图片路径
OUTPUT_PATH = os.path.join(ROOT_DIR, 'analyze', 'format', 'generated_caiwu.png')

def load_data():
    """加载财务数据"""
    # 加载财务指标数据
    financial_indicator = pd.read_csv(FINANCIAL_INDICATOR_PATH)
    # 加载资产负债表数据
    balance_sheet = pd.read_csv(BALANCE_SHEET_PATH)
    # 加载利润表数据
    income_statement = pd.read_csv(INCOME_STATEMENT_PATH)
    # 加载现金流量表数据
    cash_flow = pd.read_csv(CASH_FLOW_PATH)
    
    return {
        'financial_indicator': financial_indicator,
        'balance_sheet': balance_sheet,
        'income_statement': income_statement,
        'cash_flow': cash_flow
    }

def process_data(data):
    """处理财务数据，提取关键指标"""
    # 提取最近的年报数据
    financial_indicator = data['financial_indicator']
    balance_sheet = data['balance_sheet']
    income_statement = data['income_statement']
    cash_flow = data['cash_flow']
    
    # 检查是否存在'报告类型'列或'报告日期名称'列
    if '报告类型' in balance_sheet.columns:
        # 筛选年报数据 - 可能标记为'年报'或包含'年报'字样
        balance_sheet = balance_sheet[balance_sheet['报告类型'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
        income_statement = income_statement[income_statement['报告类型'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
        cash_flow = cash_flow[cash_flow['报告类型'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
        # 对于financial_indicator，需要检查是否有'报告类型'列
        if '报告类型' in financial_indicator.columns:
            financial_indicator = financial_indicator[financial_indicator['报告类型'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
        else:
            # 如果没有'报告类型'列，则按日期筛选年度数据
            date_col = '日期' if '日期' in financial_indicator.columns else '报告日期'
            if date_col in financial_indicator.columns:
                financial_indicator = financial_indicator[financial_indicator[date_col].str.contains('-12-31', na=False)].sort_values(date_col, ascending=False)
    elif '报告日期名称' in balance_sheet.columns:
        # 如果有'报告日期名称'列，筛选包含'年报'的行
        financial_indicator = financial_indicator[financial_indicator['报告日期名称'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
        balance_sheet = balance_sheet[balance_sheet['报告日期名称'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
        income_statement = income_statement[income_statement['报告日期名称'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
        cash_flow = cash_flow[cash_flow['报告日期名称'].str.contains('年报', na=False)].sort_values('报告日期', ascending=False)
    else:
        # 如果没有报告类型列，则按日期排序并尝试筛选年度数据（通常是每年的12-31日期）
        date_col = '日期' if '日期' in financial_indicator.columns else '报告日期'
        financial_indicator = financial_indicator[financial_indicator[date_col].str.contains('-12-31', na=False)].sort_values(date_col, ascending=False)
        balance_sheet = balance_sheet[balance_sheet['报告日期'].str.contains('-12-31', na=False)].sort_values('报告日期', ascending=False)
        income_statement = income_statement[income_statement['报告日期'].str.contains('-12-31', na=False)].sort_values('报告日期', ascending=False)
        cash_flow = cash_flow[cash_flow['报告日期'].str.contains('-12-31', na=False)].sort_values('报告日期', ascending=False)
    
    # 提取最近5年的数据
    financial_indicator = financial_indicator.head(5).iloc[::-1]
    balance_sheet = balance_sheet.head(5).iloc[::-1]
    income_statement = income_statement.head(5).iloc[::-1]
    cash_flow = cash_flow.head(5).iloc[::-1]
    
    # 提取年份 - 根据实际列名调整
    date_column = '日期' if '日期' in financial_indicator.columns else '报告日期'
    years = [str(date).split('-')[0] for date in financial_indicator[date_column]]
    
    # 提取关键财务指标 - 根据实际列名调整
    key_metrics = {}
    
    # 每股收益
    if '摊薄每股收益(元)' in financial_indicator.columns:
        key_metrics['每股收益(元)'] = financial_indicator['摊薄每股收益(元)'].values
    else:
        key_metrics['每股收益(元)'] = financial_indicator['基本每股收益'].values if '基本每股收益' in financial_indicator.columns else np.zeros(len(years))
    
    # 净资产收益率
    if '净资产收益率(%)' in financial_indicator.columns:
        key_metrics['净资产收益率(%)'] = financial_indicator['净资产收益率(%)'].values
    else:
        key_metrics['净资产收益率(%)'] = financial_indicator['加权净资产收益率(%)'].values if '加权净资产收益率(%)' in financial_indicator.columns else np.zeros(len(years))
    
    # 营业收入
    if '营业收入' in income_statement.columns:
        key_metrics['营业收入(亿元)'] = income_statement['营业收入'].values / 100  # 转换为亿元
    else:
        key_metrics['营业收入(亿元)'] = np.zeros(len(years))
    
    # 净利润
    if '净利润' in income_statement.columns:
        key_metrics['净利润(亿元)'] = income_statement['净利润'].values / 100  # 转换为亿元
    else:
        key_metrics['净利润(亿元)'] = np.zeros(len(years))
    
    # 总资产
    if '资产总计' in balance_sheet.columns:
        key_metrics['总资产(亿元)'] = balance_sheet['资产总计'].values / 100  # 转换为亿元
    else:
        key_metrics['总资产(亿元)'] = np.zeros(len(years))
    
    # 净资产
    if '权益总计' in balance_sheet.columns:
        key_metrics['净资产(亿元)'] = balance_sheet['权益总计'].values / 100  # 转换为亿元
    else:
        key_metrics['净资产(亿元)'] = np.zeros(len(years))
    
    # 经营现金流
    if '经营活动产生的现金流量净额' in cash_flow.columns:
        key_metrics['经营现金流(亿元)'] = cash_flow['经营活动产生的现金流量净额'].values / 100  # 转换为亿元
    else:
        key_metrics['经营现金流(亿元)'] = np.zeros(len(years))
    
    return years, key_metrics

def create_chart(years, key_metrics):
    """创建财务数据结构图表"""
    # 创建图表
    plt.figure(figsize=(16, 10), dpi=100, facecolor='white')
    gs = GridSpec(3, 2, height_ratios=[1, 1, 1])
    
    # 设置全局字体样式
    plt.rcParams.update({'font.size': 12})
    
    # 设置图表标题
    plt.suptitle('平安银行(000001)财务数据分析', fontsize=20, y=0.98)
    
    # 绘制每股收益和净资产收益率图表
    ax1 = plt.subplot(gs[0, 0])
    bar_width = 0.35
    x = np.arange(len(years))
    ax1.bar(x - bar_width/2, key_metrics['每股收益(元)'], bar_width, label='每股收益(元)', color='#4472C4')
    ax1.set_ylabel('每股收益(元)', color='#4472C4')
    ax1.tick_params(axis='y', labelcolor='#4472C4')
    ax1.set_xticks(x)
    ax1.set_xticklabels(years)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax1_twin = ax1.twinx()
    ax1_twin.plot(x, key_metrics['净资产收益率(%)'], 'o-', color='#ED7D31', linewidth=2, markersize=8)
    ax1_twin.set_ylabel('净资产收益率(%)', color='#ED7D31')
    ax1_twin.tick_params(axis='y', labelcolor='#ED7D31')
    
    # 添加图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + ['净资产收益率(%)'], loc='upper left')
    ax1.set_title('盈利能力', fontsize=14)
    
    # 绘制营业收入和净利润图表
    ax2 = plt.subplot(gs[0, 1])
    ax2.bar(x - bar_width/2, key_metrics['营业收入(亿元)'], bar_width, label='营业收入(亿元)', color='#4472C4')
    ax2.set_ylabel('营业收入(亿元)', color='#4472C4')
    ax2.tick_params(axis='y', labelcolor='#4472C4')
    ax2.set_xticks(x)
    ax2.set_xticklabels(years)
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax2_twin = ax2.twinx()
    ax2_twin.plot(x, key_metrics['净利润(亿元)'], 'o-', color='#ED7D31', linewidth=2, markersize=8)
    ax2_twin.set_ylabel('净利润(亿元)', color='#ED7D31')
    ax2_twin.tick_params(axis='y', labelcolor='#ED7D31')
    
    # 添加图例
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + ['净利润(亿元)'], loc='upper left')
    ax2.set_title('收入与利润', fontsize=14)
    
    # 绘制总资产和净资产图表
    ax3 = plt.subplot(gs[1, 0])
    ax3.bar(x - bar_width/2, key_metrics['总资产(亿元)'], bar_width, label='总资产(亿元)', color='#4472C4')
    ax3.set_ylabel('总资产(亿元)', color='#4472C4')
    ax3.tick_params(axis='y', labelcolor='#4472C4')
    ax3.set_xticks(x)
    ax3.set_xticklabels(years)
    ax3.grid(axis='y', linestyle='--', alpha=0.7)
    
    ax3_twin = ax3.twinx()
    ax3_twin.plot(x, key_metrics['净资产(亿元)'], 'o-', color='#ED7D31', linewidth=2, markersize=8)
    ax3_twin.set_ylabel('净资产(亿元)', color='#ED7D31')
    ax3_twin.tick_params(axis='y', labelcolor='#ED7D31')
    
    # 添加图例
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + ['净资产(亿元)'], loc='upper left')
    ax3.set_title('资产规模', fontsize=14)
    
    # 绘制经营现金流图表
    ax4 = plt.subplot(gs[1, 1])
    ax4.bar(x, key_metrics['经营现金流(亿元)'], bar_width*1.5, label='经营现金流(亿元)', color='#4472C4')
    ax4.set_ylabel('经营现金流(亿元)', color='#4472C4')
    ax4.tick_params(axis='y', labelcolor='#4472C4')
    ax4.set_xticks(x)
    ax4.set_xticklabels(years)
    ax4.grid(axis='y', linestyle='--', alpha=0.7)
    ax4.legend(loc='upper left')
    ax4.set_title('现金流', fontsize=14)
    
    # 绘制财务指标表格
    ax5 = plt.subplot(gs[2, :])
    ax5.axis('tight')
    ax5.axis('off')
    
    # 准备表格数据
    table_data = [
        ['指标'] + years,
        ['每股收益(元)'] + [f'{val:.2f}' for val in key_metrics['每股收益(元)']],
        ['净资产收益率(%)'] + [f'{val:.2f}' for val in key_metrics['净资产收益率(%)']],
        ['营业收入(亿元)'] + [f'{val:.2f}' for val in key_metrics['营业收入(亿元)']],
        ['净利润(亿元)'] + [f'{val:.2f}' for val in key_metrics['净利润(亿元)']],
        ['总资产(亿元)'] + [f'{val:.2f}' for val in key_metrics['总资产(亿元)']],
        ['净资产(亿元)'] + [f'{val:.2f}' for val in key_metrics['净资产(亿元)']],
        ['经营现金流(亿元)'] + [f'{val:.2f}' for val in key_metrics['经营现金流(亿元)']]
    ]
    
    # 创建表格
    table = ax5.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)
    
    # 设置表格样式
    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == 0:  # 表头行和第一列
            cell.set_facecolor('#4472C4')
            cell.set_text_props(color='white')
        else:
            cell.set_facecolor('#E6F0FF' if i % 2 == 0 else 'white')
    
    # 调整布局
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # 保存图表
    plt.savefig(OUTPUT_PATH, dpi=100, bbox_inches='tight')
    print(f"财务数据结构图表已保存至: {OUTPUT_PATH}")
    
    # 显示图表
    plt.close()

def main():
    try:
        # 加载数据
        data = load_data()
        
        # 处理数据
        years, key_metrics = process_data(data)
        
        # 创建图表
        create_chart(years, key_metrics)
        
        print("财务数据结构图表生成成功！")
        
    except Exception as e:
        print(f"生成财务数据结构图表时出错: {str(e)}")

if __name__ == "__main__":
    main()