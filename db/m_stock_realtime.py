import akshare as ak
import sqlite3
import os
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 数据库配置
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, 'm_stock.db')

def create_table():
    """创建数据表"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建美股实时行情表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS m_stock_realtime (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_code TEXT NOT NULL,
        stock_name TEXT,
        latest_price REAL,
        change_amount REAL,
        change_percent REAL,
        open_price REAL,
        high_price REAL,
        low_price REAL,
        prev_close REAL,
        total_market_value REAL,
        pe_ratio REAL,
        volume REAL,
        amount REAL,
        amplitude REAL,
        turnover_rate REAL,
        update_time TIMESTAMP,
        UNIQUE(stock_code, update_time)
    )
    """)
    
    # 创建索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_stock_code ON m_stock_realtime(stock_code)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_update_time ON m_stock_realtime(update_time)")
    
    conn.commit()
    conn.close()

def get_and_save_realtime_data():
    """获取并保存实时行情数据"""
    try:
        # 获取美股实时行情数据
        df = ak.stock_us_spot_em()
        
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 获取当前时间
        current_time = datetime.now()
        
        # 准备数据并插入
        for _, row in df.iterrows():
            # 处理股票代码，移除前缀的数字和点号
            stock_code = str(row['代码'])
            if '.' in stock_code:
                stock_code = stock_code.split('.')[-1]

            data = (
                stock_code,
                str(row['名称']),
                float(row['最新价']),
                float(row['涨跌额']),
                float(row['涨跌幅']),
                float(row['开盘价']),
                float(row['最高价']),
                float(row['最低价']),
                float(row['昨收价']),
                float(row['总市值']),
                float(row['市盈率']),
                float(row['成交量']),
                float(row['成交额']),
                float(row['振幅']),
                float(row['换手率']),
                current_time
            )
            
            try:
                cursor.execute("""
                INSERT INTO m_stock_realtime 
                (stock_code, stock_name, latest_price, change_amount, 
                change_percent, open_price, high_price, low_price, 
                prev_close, total_market_value, pe_ratio, volume, 
                amount, amplitude, turnover_rate, update_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data)
            except sqlite3.IntegrityError:
                logging.warning(f"重复数据，股票代码: {data[0]}, 时间: {current_time}")
                continue
            except Exception as e:
                logging.error(f"插入数据失败，股票代码: {data[0]}, 错误: {str(e)}")
                continue
        
        conn.commit()
        conn.close()
        logging.info(f"成功更新 {len(df)} 条美股实时行情数据")
        
    except Exception as e:
        logging.error(f"获取或保存数据失败: {str(e)}")

def main():
    # 确保数据库目录存在
    os.makedirs(DB_DIR, exist_ok=True)
    
    # 创建数据表
    create_table()
    
    # 获取并保存数据
    get_and_save_realtime_data()

if __name__ == "__main__":
    main()