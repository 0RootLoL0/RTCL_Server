import configparser, json

def createConfig(path):
    config = configparser.ConfigParser()
    config.add_section("server")
    config.set("server", "urldb", input())
    config.set("server", "prefixdb", input())

    with open(path, "w") as config_file:
        config.write(config_file)
 
 
if __name__ == "__main__":
    path = "rtclServer.conf"
    createConfig(path)

"""
    import configparser

config = configparser.ConfigParser()
config.read("config.ini")

config.get("Bot", "token")
    
"""