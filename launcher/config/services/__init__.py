"""
服务配置过滤器集合。

该模块包含多个服务（Flask、Ollama、PostgreSQL 等）的配置提取器，
从统一的 env_dict 中解析出每个服务所需字段，进行封装和类型转换。

推荐用法：
    from config.services import flask_config_from, pg_config_from
    flask_cfg = flask_config_from(env_dict)
"""
