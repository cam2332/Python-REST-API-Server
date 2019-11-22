from configparser import ConfigParser
import socket

def configDB(filename='Properties.ini', section='postgresql'):
    parser = ConfigParser()

    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section,filename))

    return db

def configSERVER(element, filename='Properties.ini', section='server'):
    parser = ConfigParser()

    parser.read(filename)

    server = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            server[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return server[element]

def configLocalIP():
    return [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]