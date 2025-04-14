
import configparser

def read_properties(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config
