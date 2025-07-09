from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import argparse

app = Flask(__name__)
CORS(app)  # 解决跨域问题

def get_db_connection():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'default.db'))
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/settings', methods=['GET'])
def get_settings():
    conn = get_db_connection()
    settings = conn.execute('SELECT * FROM server_config LIMIT 1').fetchone()
    conn.close()
    
    if settings is None:
        return jsonify({
            'serverIp': '127.0.0.1',
            'serverPort': 8080,
            'timeout': 10,
            'logDirectory': '/var/log/server-monitor',
            'enableCompression': True,
            'enableCache': False,
            'autoReconnect': True
        })
        
    return jsonify({
        'display_name': settings['display_name'],
        'serverIp': settings['server_host'],
        'serverPort': settings['server_port'],
        'timeout': settings['connection_timeout'],
        'logDirectory': settings['log_directory'],
        'enableCompression': settings['enable_compression'] == 1,
        'enableCache': settings['enable_cache'] == 1,
        'autoReconnect': settings['auto_reconnect'] == 1
    })

@app.route('/api/settings', methods=['POST'])
def save_settings():
    data = request.get_json()
    conn = get_db_connection()
    
    try:
        # 检查是否已有设置记录
        existing = conn.execute('SELECT id FROM server_config LIMIT 1').fetchone()
        
        # 定义前端参数到数据库字段的映射
        field_mapping = {
            'display_name': 'display_name',
            'serverIp': 'server_host',
            'serverPort': 'server_port',
            'timeout': 'connection_timeout',
            'logDirectory': 'log_directory',
            'enableCompression': 'enable_compression',
            'enableCache': 'enable_cache',
            'autoReconnect': 'auto_reconnect'
        }
        
        if existing:
            # 收集要更新的字段和值
            update_fields = []
            params = []
            
            for frontend_key, db_column in field_mapping.items():
                if frontend_key in data:
                    update_fields.append(f"{db_column} = ?")
                    # 处理布尔值转换
                    if frontend_key in ['enableCompression', 'enableCache', 'autoReconnect']:
                        params.append(1 if data[frontend_key] else 0)
                    else:
                        params.append(data[frontend_key])
            
            if update_fields:
                # 添加WHERE子句的参数
                params.append(existing['id'])
                # 构建动态SQL语句
                sql = f"UPDATE server_config SET {', '.join(update_fields)} WHERE id = ?"
                cursor = conn.execute(sql, params)
                # 添加调试信息
                print(f"Executing SQL: {sql}")
                print(f"Params: {params}")
                print(f"Rows affected: {cursor.rowcount}")
        else:
            # 创建新设置记录 - 使用默认值填充缺失字段
            default_values = {
                'display_name': '服务器监控系统',
                'serverIp': '127.0.0.1',
                'serverPort': 8080,
                'timeout': 10,
                'logDirectory': '/var/log/server-monitor',
                'enableCompression': True,
                'enableCache': False,
                'autoReconnect': True
            }
            
            # 合并默认值和请求数据
            insert_data = {** default_values, **data}
            conn.execute(
                'INSERT INTO server_config (display_name, server_host, server_port, connection_timeout, log_directory, enable_compression, enable_cache, auto_reconnect) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    insert_data['display_name'],
                    insert_data['serverIp'],
                    insert_data['serverPort'],
                    insert_data['timeout'],
                    insert_data['logDirectory'],
                    1 if insert_data['enableCompression'] else 0,
                    1 if insert_data['enableCache'] else 0,
                    1 if insert_data['autoReconnect'] else 0
                )
            )
        
        conn.commit()
        return jsonify({
            'status': 'success', 
            'message': 'Settings saved successfully',
            'updated_fields': {k: data[k] for k in data if k in field_mapping}
        })
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()
    app.run(debug=True, port=args.port)