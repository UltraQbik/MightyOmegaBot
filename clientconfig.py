import os
import configparser


def parse_config_file(filepath: str):
    config = configparser.ConfigParser()
    config.read(filepath, encoding="utf-8")
    return config


def get_config():
    config = {}
    for file in os.listdir("client_configs"):
        if os.path.isfile(f"client_configs/{file}"):
            config[os.path.splitext(file)[0]] = parse_config_file(f"client_configs/{file}")
    return config
