import sys, yaml
from easysnmp import Session


def get_port_index(session, port):
    port_number = port.split('/')[-1]
    rx_tag = ' ' + port_number + ' Rx'
    receive_tag = '/' + port_number + ' Receive'
    rx_tags = [rx_tag, receive_tag]

    # walk entity-mib
    walk = session.walk(config['entity_mib'])

    # filter entity-mib for port index
    for snmpvar in walk:
        if any(tag in snmpvar.value for tag in rx_tags):
            port_oid = snmpvar.oid

    port_index = port_oid.split('.')[-1]
    return port_index


def get_port_light_lvl(session, port):
    port_index = get_port_index(session, port)
    light_lvl_oid = config['light_lvl_mib'] + port_index
    get = session.get(light_lvl_oid)
    light_lvl = float(get.value) / 10
    return(light_lvl)


if __name__ == '__main__':

    with open('config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    print(config['csv_header'])

    node_port_csv = sys.argv[1]

    with open(node_port_csv, 'r') as csv:
        for row in csv.readlines():
            columns = row.split(',')
            host = columns[0]
            fqdn = host + config['domain']
            port = columns[1].split('\n')[0]

            session = Session(hostname=fqdn, community=config['snmp_community'], version=2)

            port_light_lvl = str(get_port_light_lvl(session, port))

            print(host + ',' + port + ',' + port_light_lvl)
