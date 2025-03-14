import pandas as pd
import os

def transform_cash_flow(file_path):
    # 读取CSV文件
    df = pd.read_csv(file_path)
    
    # 获取所有日期
    dates = df['REPORT_DATE_NAME'].unique()
    
    # 获取需要转置的列名（排除非数据列）
    exclude_cols = ['SECUCODE', 'SECURITY_CODE', 'SECURITY_NAME_ABBR', 'ORG_CODE', 
                   'ORG_TYPE', 'REPORT_DATE', 'REPORT_TYPE', 'REPORT_DATE_NAME', 
                   'SECURITY_TYPE_CODE', 'NOTICE_DATE', 'UPDATE_DATE', 'CURRENCY',
                   'OPINION_TYPE', 'OSOPINION_TYPE']
    data_cols = [col for col in df.columns if col not in exclude_cols and not col.endswith('_YOY')]
    
    # 创建新的DataFrame
    transformed_data = []
    
    def format_to_hundred_million(value):
        try:
            num = float(value)
            # 所有数值都转换为亿为单位
            return round(num / 100000000, 2)  # 转换为亿并保留两位小数
        except (ValueError, TypeError):
            return value
    
    # 对每个指标进行处理
    for col in data_cols:
        row_data = {'指标名称': col}
        # 获取每个日期的值
        for date in sorted(dates, reverse=True):
            # 获取指定日期的数据
            date_data = df[df['REPORT_DATE_NAME'] == date]
            # 检查是否存在数据
            try:
                value = date_data[col].iloc[0] if not date_data.empty else None
                row_data[date] = format_to_hundred_million(value)
            except Exception as e:
                print(f"处理数据时出错: {e}")
        transformed_data.append(row_data)
    
    # 转换为DataFrame
    result_df = pd.DataFrame(transformed_data)
    
    # 设置指标名称为索引
    result_df.set_index('指标名称', inplace=True)
    
    return result_df

def main():
    # 获取当前目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'finance_data/A_600519/600519_cash_flow.csv')
    output_file = os.path.join(base_dir, 'finance_data/A_600519/600519_cash_flow_transformed.csv')
    
    # 转换数据
    transformed_df = transform_cash_flow(input_file)
    
    # 保存结果
    transformed_df.to_csv(output_file, encoding='utf-8-sig')
    print(f'转换完成，结果已保存至：{output_file}')

if __name__ == '__main__':
    main()