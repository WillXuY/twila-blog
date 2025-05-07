from application import create_app

# 创建 Flask 应用实例
app = create_app()

# 这里通常不会直接运行应用，而是通过 WSGI 服务器来启动
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
