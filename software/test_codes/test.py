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
    config.add_section("DbId")
    config.set("DbId", "id", "0" )
    
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
 

def post_request(event_time, feeder_type, serial_number, feed_time, animal_id, end_weight, feed_weight):
    try:
        payload = {
            "Eventdatetime": event_time,
            "EquipmentType": feeder_type,
            "SerialNumber": serial_number,
            "FeedingTime": feed_time,
            "RFIDNumber": animal_id,
            "WeightLambda": end_weight,
            "FeedWeight": feed_weight
        }
        return payload
    except ValueError as v:
        logger.error(f'Post_request function error: {v}')


def main():
    dbid = 0
    while(dbid < 20):
        path = 'config.ini'
        section = "Calibration"
        if not os.path.exists(path):
            create_config(path)
        config = configparser.ConfigParser()
        config.read(path)
        offset = float(config.get(section, "Offset"))
        scale = float(config.get(section, "Scale"))
        dbid = int(config.get("DbId", "id"))
        print(f'DBID = {dbid}')
        dbid+=1
        print(f'DBID = {dbid}')
        print(offset, scale)
        print(type(offset), type(scale))
        print("Here we have a new offset and scale value!")
        offset = 11111.11
        scale = 2222.22
        update_setting(path, section, "Offset", offset)
        update_setting(path, section, "Scale", scale)
        update_setting(path, "DbId", "id", str(dbid))
        offset = float(get_setting(path, section, "Offset"))
        scale = float(get_setting(path, section, "Scale"))
        print(f'DBID in config.ini = {int(get_setting(path, "DbId", "id"))}')
        print(offset, scale)
        print(type(offset), type(scale))



main()
    