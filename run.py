from common import get_config

if __name__ == "__main__":
    configs = get_config()
    for key, value in configs.items():
        if key == "uid":  # 排除掉 uid 的配置
            continue
        module = __import__(f"scripts.{key}", fromlist=["*"])
        main = getattr(module, "main")
        main()
