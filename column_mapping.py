import pandas as pd

def load_mapping_file(file_path):
    """加载映射文件，返回英文到中文的映射字典"""
    mapping_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # 跳过空行
                en, cn = line.split('\t')
                mapping_dict[en] = cn
    return mapping_dict

def process_numeric_data(value):
    """处理数值数据：整数转换为亿为单位，小数保留两位
    支持处理：
    1. 带逗号的数字 (如 1,234.56)
    2. 科学计数法 (如 1.23e8)
    3. 空值处理
    4. 非数值型数据处理
    """
    try:
        # 处理空值
        if pd.isna(value) or value == '':
            return value
            
        # 将输入转换为字符串并移除逗号
        str_value = str(value).replace(',', '')
        
        # 转换为浮点数（自动处理科学计数法）
        num = float(str_value)
        
        # 转换为亿为单位并保留两位小数
        result = round(num / 100000000, 2)
        
        # 处理极小值，避免显示为科学计数法
        if abs(result) < 0.01 and result != 0:
            return 0.01 if result > 0 else -0.01
            
        return result
        
    except (ValueError, TypeError):
        # 如果无法转换为数值，则返回原值
        return value

def process_numeric_columns(df):
    """处理DataFrame中'货币单位'列之后的数值列
    
    Args:
        df: pandas DataFrame对象
    Returns:
        处理后的DataFrame
    """
    unit_index = -1
    for i, col in enumerate(df.columns):
        if '货币单位' in col:
            unit_index = i
            break

    if unit_index != -1:
        # 处理'货币单位'之后的数值列
        numeric_columns = df.columns[unit_index + 1:]
        for col in numeric_columns:
            df[col] = df[col].apply(process_numeric_data)
    return df

def map_columns(df, mapping_dict):
    """根据映射字典转换DataFrame的列名，并只保留有映射关系且非空的列，同时处理数值列"""
    # 获取有映射关系的列
    valid_columns = [col for col in df.columns if col in mapping_dict]
    
    # 只保留有映射关系的列
    df = df[valid_columns]
    
    # 删除全部为空值的列
    df = df.dropna(axis=1, how='all')
    
    # 更新有效列列表（排除已删除的空列）
    valid_columns = [col for col in valid_columns if col in df.columns]
    
    # 重命名列
    column_mapping = {col: mapping_dict[col] for col in valid_columns}
    df = df.rename(columns=column_mapping)
    
    return df