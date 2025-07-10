import sqlite3
import os

def create_database(app):
    # 连接数据库（如果不存在则创建）
    db_path = os.path.join(os.path.dirname(__file__), 'default.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 安全地创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        # 安全地创建服务器配置表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS server_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            display_name TEXT NOT NULL,
            refresh_rate INTEGER DEFAULT 5,
            show_cpu_usage INTEGER DEFAULT 1,
            show_memory_usage INTEGER DEFAULT 1,
            show_disk_usage INTEGER DEFAULT 1,
            show_network_usage INTEGER DEFAULT 1,
            show_process_list INTEGER DEFAULT 1,
            enable_alerts INTEGER DEFAULT 1,
            alert_on_high_cpu INTEGER DEFAULT 1,
            alert_on_high_memory INTEGER DEFAULT 1,
            alert_on_high_disk INTEGER DEFAULT 1,
            server_host TEXT DEFAULT 'localhost',
            server_port INTEGER DEFAULT 15600,
            connection_timeout INTEGER DEFAULT 30,
            max_connections INTEGER DEFAULT 10,
            log_directory TEXT DEFAULT '',
            enable_compression INTEGER DEFAULT 1,
            enable_cache INTEGER DEFAULT 1,
            auto_reconnect INTEGER DEFAULT 1
        )
        ''')

        # 使用参数化查询插入初始配置 - 防止SQL注入
        initial_config = {
            'display_name': '服务器监控系统',
            'refresh_rate': 5,
            'show_cpu_usage': 1,
            'show_memory_usage': 1,
            'show_disk_usage': 1,
            'show_network_usage': 1,
            'show_process_list': 1,
            'enable_alerts': 1,
            'alert_on_high_cpu': 1,
            'alert_on_high_memory': 1,
            'alert_on_high_disk': 1,
            'server_host': 'localhost',
            'server_port': 15600,
            'connection_timeout': 30,
            'max_connections': 10,
            'log_directory': '/var/log/operation_log',
            'enable_compression': 1,
            'enable_cache': 1,
            'auto_reconnect': 1
        }

        # 检查是否已存在配置（使用参数化查询）
        cursor.execute("SELECT COUNT(*) FROM server_config")
        if cursor.fetchone()[0] == 0:
            # 使用命名占位符的参数化查询
            cursor.execute('''
            INSERT INTO server_config (
                display_name, refresh_rate, show_cpu_usage, show_memory_usage,
                show_disk_usage, show_network_usage, show_process_list, enable_alerts,
                alert_on_high_cpu, alert_on_high_memory, alert_on_high_disk,
                server_host, server_port, connection_timeout, max_connections,
                log_directory, enable_compression, enable_cache, auto_reconnect
            ) VALUES (
                :display_name, :refresh_rate, :show_cpu_usage, :show_memory_usage,
                :show_disk_usage, :show_network_usage, :show_process_list, :enable_alerts,
                :alert_on_high_cpu, :alert_on_high_memory, :alert_on_high_disk,
                :server_host, :server_port, :connection_timeout, :max_connections,
                :log_directory, :enable_compression, :enable_cache, :auto_reconnect
            )
            ''', initial_config)

        # 提交更改
        conn.commit()
        app.logger.warning("sql: 数据库创建成功！配置表已安全初始化。数据库路径: %s", db_path)
        
    except sqlite3.Error as e:
        app.logger.error("sql: 数据库错误: %s", e)
        conn.rollback()
    finally:
        # 确保连接关闭
        conn.close()

# def safe_query_config():
#     """安全查询配置的示例函数"""
#     try:
#         conn = sqlite3.connect('default.db')
#         cursor = conn.cursor()
        
#         # 使用参数化查询
#         cursor.execute("SELECT * FROM server_config WHERE id = ?", (1,))
#         config = cursor.fetchone()
        
#         if config:
#             print("\n安全查询结果:")
#             print(f"服务器名称: {config[1]}")
#             print(f"刷新频率: 每 {config[2]} 秒")
#             print(f"监控CPU: {'启用' if config[3] else '禁用'}")
#         else:
#             print("未找到配置")
            
#     except sqlite3.Error as e:
#         print(f"查询出错: {e}")
#     finally:
#         conn.close()

# def safe_update_config(param, value):
#     """安全更新配置的示例函数"""
#     try:
#         conn = sqlite3.connect('default.db')
#         cursor = conn.cursor()
    
            
#         # 参数化更新
#         cursor.execute(f"UPDATE server_config SET {param} = ? WHERE id = ?", (value, 1))
#         conn.commit()
#         print(f"已安全更新 {param} 为 {value}")
        
#     except sqlite3.Error as e:
#         print(f"更新出错: {e}")
#         conn.rollback()
#     finally:
#         conn.close()

if __name__ == "__main__":
    # 创建并初始化数据库
    create_database()
    
    
    # # 演示安全更新
    # safe_update_config('display_name', '服务器')  # 合法更新