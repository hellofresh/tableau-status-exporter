from prometheus_client.core import GaugeMetricFamily


class TableauServerStatusParser(object):
    DEFAULT_LABEL_KEYS = ['machine', 'process', 'status']

    STATUS_MAP = {
        'Active': 0,
        'Busy': 0,
        'Passive': 0,
        'Unlicensed': 0,
        'Down': 0,
        'ReadOnly': 0,
        'ActiveSyncing': 0,
        'StatusNotAvailable': 0,
        'StatusNotAvailableSyncing': 0,
        'NotAvailable': 0,
        'DecommisionedReadOnly': 0,
        'DecomisioningReadOnly': 0,
        'DecommissionFailedReadOnly' :0
    }

    @staticmethod
    def init_process_map(machine, process_map, status_map=STATUS_MAP):
        """
        Initiates server processes status dictionary.
        Arguments:
            object(machine): object to parse
            process_map(dictionary): skeleton dictionary
            status_map(dictionary): Dictionary with status counts (initial)
        Returns:
            status_map(dictionary): Dictionary with status counts (actual)
        """
        for process in machine:
            # init
            if process.tag not in process_map:
                process_map[process.tag] = dict(status_map)
            # increment
            process_map[process.tag][process.attrib['status']] += 1
        return process_map

    @staticmethod
    def tableau_server_parse_status_metrics(xml_response, labels=DEFAULT_LABEL_KEYS):
        """
        Parses Tableau Server statuses.
        Arguments:
            object(xml_response): object to parse
            labels (list[string]): metric labels
        Returns:
            Generators[GaugeMetricFamily]: generators of prometheus metrics
        """
        name = 'tableau_server_process_status'
        server_status = GaugeMetricFamily(
          name,
          'Process status',
          labels = labels
        )
        for machine in xml_response:
            process_map = {}
            machine_name = machine.attrib['name']
            process_map = TableauServerStatusParser.init_process_map(machine, process_map)
            for process in process_map:
                for process_status in process_map[process]:
                    server_status.add_metric([machine_name, process, process_status],
                        process_map[process][process_status])
        return server_status
