import configparser
import os


def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Calibration")
    config.set("Calibration", "Offset", "0")
    config.set("Calibration", "Scale", "0" )
    
    with open(path, "w") as config_file:
        config.write(config_file)
 
 
def get_config(path):
    """
    Returns the config object
    """
    if not os.path.exists(path):
        create_config(path)
    
    config = configparser.ConfigParser()
    config.read(path)
    return config
 
 
def get_setting(path, section, setting):
    """
    Get value from setting
    """
    config = get_config(path)
    value = config.get(section, setting)

    return value
 
 
def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, str(value))
    with open(path, "w") as config_file:
        config.write(config_file)
 


def main():
    path = 'config.ini'
    section = "Calibration"
    if not os.path.exists(path):
        create_config(path)
    config = configparser.ConfigParser()
    config.read(path)
    offset = float(config.get(section, "Offset"))
    scale = float(config.get(section, "Scale"))
    print(offset, scale)
    print(type(offset), type(scale))
    print("Here we have a new offset and scale value!")
    offset = 11111.11
    scale = 2222.22
    update_setting(path, section, "Offset", offset)
    update_setting(path, section, "Scale", scale)
    offset = float(get_setting(path, section, "Offset"))
    scale = float(get_setting(path, section, "Scale"))
    print(offset, scale)
    print(type(offset), type(scale))



main()
    