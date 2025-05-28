from application import create_app

# 创建 Flask 应用实例
app = create_app()

# 开发环境下运行 debug 模式
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
