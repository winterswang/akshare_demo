import pandas as pd
import os

def process_numeric_data(value):
    """处理数值数据：整数转换为亿为单位，小数保留两位"""
    try:
        # 将字符串转换为浮点数
        num = float(value)
        # 判断是否为整数
        if num.is_integer():
            # 转换为亿为单位
            return round(num / 100000000, 2)
        else:
            # 保留两位小数
            return round(num, 2)
    except (ValueError, TypeError):
        # 如果无法转换为数值，则返回原值
        return value

def process_finance_file(file_path):
    """处理单个财务文件"""
    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 获取所有列名
        columns = df.columns.tolist()
        
        # 找到'货币单位'所在的位置
        unit_index = -1
        for i, col in enumerate(columns):
            if '货币单位' in col:
                unit_index = i
                break
        
        if unit_index == -1:
            print(f"在文件 {file_path} 中未找到'货币单位'列")
            return
        
        # 处理'货币单位'之后的数值列
        numeric_columns = columns[unit_index + 1:]
        for col in numeric_columns:
            df[col] = df[col].apply(process_numeric_data)
        
        # 构建新文件名
        base_name, ext = os.path.splitext(file_path)
        new_file_path = f"{base_name}_fix{ext}"
        
        # 保存处理后的数据
        df.to_csv(new_file_path, index=False)
        print(f"已处理并保存文件：{new_file_path}")
        
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误：{str(e)}")

def main():
    # 获取finance目录下的所有文件
    finance_dir = 'finance'
    file_types = ['cash_flow']
    
    for file_type in file_types:
        # 查找对应类型的文件
        for file_name in os.listdir(finance_dir):
            if file_type in file_name and not file_name.endswith('_fix.csv'):
                file_path = os.path.join(finance_dir, file_name)
                process_finance_file(file_path)

if __name__ == '__main__':
    main()