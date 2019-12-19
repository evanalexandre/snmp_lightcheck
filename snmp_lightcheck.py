import sys, yaml
from easysnmp import Session


class OpticTransceiver:

    def __init__(self, node, port):

        self.node = node
        self.port = port
        self.fqdn = node + config['domain']
        self.session = self.get_session()
        self.port_index = self.get_port_index()


    def get_session(self):
        
        self.session = Session(hostname=self.fqdn, community=config['snmp_community'], version=2)
        return self.session

    def get_port_index(self):

        port_number = self.port.split('/')[-1]
        rx_tag = ' ' + port_number + ' Rx'
        receive_tag = '/' + port_number + ' Receive'
        rx_tags = [rx_tag, receive_tag]

        # walk entity-mib
        walk = self.session.walk(config['entity_mib'])

        # filter entity-mib for port index
        for snmpvar in walk:
            if any(tag in snmpvar.value for tag in rx_tags):
                port_oid = snmpvar.oid

        port_index = port_oid.split('.')[-1]
        return port_index


    def poll_light_lvl(self):

        port_lvl_oid = config['light_lvl_mib'] + self.port_index
        get = self.session.get(port_lvl_oid)
        light_lvl = float(get.value) / 10
        return(light_lvl)


    def poll_low_warn_threshold(self):
        port_threshold_oid = config['light_threshold_mib'] + self.port_index + '.'
        low_warn_oid = port_threshold_oid + '3'
        get = self.session.get(low_warn_oid)
        low_warn = float(get.value) / 10
        return(low_warn)

    def poll_thresholds(self):
        port_threshold_oid = config['light_threshold_mib'] + self.port_index + '.'
        high_warn_oid = port_threshold_oid + '1'
        high_alarm_oid = port_threshold_oid + '2'
        low_warn_oid = port_threshold_oid + '3'
        low_alarm_oid = port_threshold_oid + '4'
        get = self.session.get(low_warn_oid)
        low_warn = float(get.value) / 10
        return(low_warn)


if __name__ == '__main__':

    with open('config.yml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    print(config['csv_header'])

    node_port_csv = sys.argv[1]

    with open(node_port_csv, 'r') as csv:
        for row in csv.readlines():
            columns = row.split(',')
            host = columns[0]
            port = columns[1].split('\n')[0]
            optic = OpticTransceiver(host, port)
            optic_lvl = str(optic.poll_light_lvl())
            optic_low_warn = str(optic.poll_low_warn_threshold())
            print(host + ',' + port + ',' + optic_lvl + ',' + optic_low_warn)
