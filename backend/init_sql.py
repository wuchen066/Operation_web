import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'default.db')

def clear_database():
    # 检查数据库文件是否存在
    if not os.path.exists(DB_PATH):
        print(f'数据库文件 {DB_PATH} 不存在，无需清理。')
        return

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 禁用外键约束以避免删除顺序问题
        cursor.execute('PRAGMA foreign_keys = OFF;')

        # 获取所有用户表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()

        if not tables:
            print('数据库中没有表需要删除。')
            return

        # 删除所有表
        table_names = [table[0] for table in tables]
        print(f'找到 {len(table_names)} 个表需要删除: {table_names}')

        for table_name in table_names:
            cursor.execute(f'DROP TABLE IF EXISTS {table_name};')
            print(f'已删除表: {table_name}')

        # 提交事务
        conn.commit()
        print('所有表已成功删除。')

    except sqlite3.Error as e:
        print(f'数据库操作失败: {e}')
        conn.rollback()
    finally:
        # 重新启用外键约束
        cursor.execute('PRAGMA foreign_keys = ON;')
        # 关闭连接
        conn.close()

if __name__ == '__main__':
    clear_database()