from flask import Flask, jsonify, request, session
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import os
import argparse
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

# 导入数据库创建函数
from sql import create_database
from flask_wtf.csrf import generate_csrf

app = Flask(__name__)

# 确保密钥已设置
app.secret_key = os.environ.get('SECRET_KEY', 'dev_key_for_testing_only')

# 数据库连接函数
def get_db_connection():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'default.db'))
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库表结构
with app.app_context():
    create_database(app)

# 初始化默认用户
def init_default_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查是否已有用户
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # 生成复杂随机用户名和密码
        username = random.choices(string.ascii_letters + string.digits, k=8)
        # username = 'admin_' + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        password = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + 
            string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?', 
            k=16
        ))
        
        # 加密密码
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')
        
        # 存储到数据库
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        print(f"app: 首次运行：已创建默认管理员用户\n用户名: {username}\n密码: {password}\n请妥善保存此凭证！")
        # app.logger.info(f"app: 首次运行：已创建默认管理员用户\n用户名: {username}\n密码: {password}\n请妥善保存此凭证！")
    
    conn.close()

# 在应用上下文中初始化默认用户
with app.app_context():
    init_default_user()

# 限制仅允许前端开发服务器访问API
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5174", "supports_credentials": True}})

# 初始化CSRF保护
csrf = CSRFProtect(app)

# 配置请求速率限制
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# 配置日志
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_request():
    app.logger.info(f"{request.method} {request.path} - {get_remote_address()}")

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 添加调试日志
    app.logger.info(f"login: 登录尝试 - 用户名: {username}, 密码长度: {len(password) if password else 0}")
    
    if not username or not password:
        app.logger.warning("login: 用户名或密码为空")
        return jsonify({'status': 'error', 'message': '用户名和密码不能为空'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if user:
        app.logger.info(f"login: 找到用户: {user['username']}, 密码哈希: {user['password_hash'][:20]}...")
        password_match = check_password_hash(user['password_hash'], password)
        app.logger.info(f"login: 密码验证结果: {password_match}")
    else:
        app.logger.warning(f"login: 未找到用户: {username}")
    
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        app.logger.info(f"login: 用户 {username} 登录成功")
        return jsonify({'status': 'success', 'message': '登录成功'})
    
    app.logger.warning(f"login: 用户 {username} 登录失败")
    return jsonify({'status': 'error', 'message': '用户名或密码错误'}), 401

@app.route('/api/login', methods=['GET'])
@limiter.limit("300 per hour")
def check_login():
    # 生成CSRF令牌
    csrf_token = generate_csrf()
    
    # 检查登录状态并获取用户名
    logged_in = 'user_id' in session
    username = ''
    
    if logged_in:
        conn = get_db_connection()
        user = conn.execute('SELECT username FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        if user:
            username = user['username']
    
    # 构建响应
    response = jsonify({
        'status': 'success',
        'logged_in': logged_in,
        'username': username
    })
    response.set_cookie('csrf_token', csrf_token, path='/')
    return response

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    app.logger.info("login: 用户登出成功")
    return jsonify({'status': 'success', 'message': '登出成功'})

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
            'logDirectory': '/var/log/operation_log',
            'enableCompression': True,
            'enableCache': False,
            'autoReconnect': True,
            'showCpuUsage': True,
            'showMemoryUsage': True,
            'showDiskUsage': True,
            'showNetworkUsage': True,
            'showProcessList': True
        })
        
    return jsonify({
        'display_name': settings['display_name'],
        'refresh_rate': settings['refresh_rate'],
        'serverIp': settings['server_host'],
        'serverPort': settings['server_port'],
        'timeout': settings['connection_timeout'],
        'logDirectory': settings['log_directory'],
        'enableCompression': settings['enable_compression'] == 1,
        'enableCache': settings['enable_cache'] == 1,
        'autoReconnect': settings['auto_reconnect'] == 1,
        'showCpuUsage': settings['show_cpu_usage'] == 1,
        'showMemoryUsage': settings['show_memory_usage'] == 1,
        'showDiskUsage': settings['show_disk_usage'] == 1,
        'showNetworkUsage': settings['show_network_usage'] == 1,
        'showProcessList': settings['show_process_list'] == 1
    })

@app.route('/api/settings', methods=['POST'])
def save_settings():
    data = request.get_json()
    conn = get_db_connection()
    
    # 输入验证
    validation_errors = []
    if 'refresh_rate' in data and (not isinstance(data['refresh_rate'], int) or data['refresh_rate'] < 1 or data['refresh_rate'] > 300):
        validation_errors.append('刷新频率必须是1-300之间的整数')
    if 'serverPort' in data and (not isinstance(data['serverPort'], int) or data['serverPort'] < 1 or data['serverPort'] > 65535):
        validation_errors.append('服务器端口必须是1-65535之间的整数')
    if 'timeout' in data and (not isinstance(data['timeout'], int) or data['timeout'] < 1 or data['timeout'] > 300):
        validation_errors.append('超时时间必须是1-300之间的整数')
    
    if validation_errors:
        return jsonify({'status': 'error', 'message': '; '.join(validation_errors)}), 400
    
    try:
        # 检查是否已有设置记录
        existing = conn.execute('SELECT id FROM server_config LIMIT 1').fetchone()
        
        # 定义前端参数到数据库字段的映射
        field_mapping = {
            'display_name': 'display_name',
            'refresh_rate': 'refresh_rate',
            'serverIp': 'server_host',
            'serverPort': 'server_port',
            'timeout': 'connection_timeout',
            'logDirectory': 'log_directory',
            'enableCompression': 'enable_compression',
            'enableCache': 'enable_cache',
            'autoReconnect': 'auto_reconnect',
            'showCpuUsage': 'show_cpu_usage',
            'showMemoryUsage': 'show_memory_usage',
            'showDiskUsage': 'show_disk_usage',
            'showNetworkUsage': 'show_network_usage',
            'showProcessList': 'show_process_list',
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
                'refresh_rate': 1,
                'serverIp': '127.0.0.1',
                'serverPort': 8080,
                'timeout': 10,
                'logDirectory': '/var/log/server-monitor',
                'enableCompression': True,
                'enableCache': False,
                'autoReconnect': True,
                'showCpuUsage': True,
                'showMemoryUsage': True,
                'showDiskUsage': True,
                'showNetworkUsage': True,
                'showProcessList': True

            }
            
            # 合并默认值和请求数据
            insert_data = {** default_values, **data}
            conn.execute(
                'INSERT INTO server_config (display_name, refresh_rate, server_host, server_port, connection_timeout, log_directory, enable_compression, enable_cache, auto_reconnect) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    insert_data['display_name'],
                    insert_data['refresh_rate'],
                    insert_data['serverIp'],
                    insert_data['serverPort'],
                    insert_data['timeout'],
                    insert_data['logDirectory'],
                    1 if insert_data['enableCompression'] else 0,
                    1 if insert_data['enableCache'] else 0,
                    1 if insert_data['autoReconnect'] else 0,
                    1 if insert_data['showCpuUsage'] else 0,
                    1 if insert_data['showMemoryUsage'] else 0,
                    1 if insert_data['showDiskUsage'] else 0,
                    1 if insert_data['showNetworkUsage'] else 0,
                    1 if insert_data['showProcessList'] else 0,
                )
            )
        
        conn.commit()
        return jsonify({
            'status': 'success', 
            'message': '保存成功',
            # 'updated_fields': {k: data[k] for k in data if k in field_mapping}
        })
    except sqlite3.Error as e:
            conn.rollback()
            app.logger.error(f"sql: 保存设置失败: {e}")
            return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500
    finally:
            conn.close()

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

if __name__ == '__main__':
    # 从环境变量获取配置
    debug_mode = True  # 临时启用调试模式以捕获错误
    secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key_change_in_production')
    
    # 设置安全密钥
    app.secret_key = secret_key
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5003, help='Port to run the server on')
    args = parser.parse_args()
    print(f"Starting server with debug_mode={debug_mode}, port={args.port}")
    app.run(host='127.0.0.1', port=args.port, debug=debug_mode)
    