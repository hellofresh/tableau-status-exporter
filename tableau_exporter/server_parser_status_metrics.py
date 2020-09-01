from prometheus_client.core import GaugeMetricFamily


class TableauServerStatusParser(object):
    DEFAULT_LABEL_KEYS = ['machine', 'process', 'status']

    STATUS_MAP = [
        'Active',
        'Busy',
        'Passive',
        'Unlicensed',
        'Down',
        'ReadOnly',
        'ActiveSyncing',
        'StatusNotAvailable',
        'StatusNotAvailableSyncing',
        'NotAvailable',
        'DecommisionedReadOnly',
        'DecomisioningReadOnly',
        'DecommissionFailedReadOnly'
        ]


    @staticmethod
    def init_process_map(machine, status_map=STATUS_MAP):
        """
        Initiates server processes status dictionary.
        Arguments:
            object(machine): object to parse
            status_map(list): List with possible process statuses
        Returns:
            status_map(dictionary): Dictionary with status counts (actual)
        """
        process_map = {}
        for process in machine:
            # init
            if process.tag not in process_map:
                process_map[process.tag] = {x :0 for x in status_map}
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
            machine_name = machine.attrib['name']
            process_map = TableauServerStatusParser.init_process_map(machine)
            for process in process_map:
                for process_status in process_map[process]:
                    server_status.add_metric([machine_name, process, process_status],
                        process_map[process][process_status])
        return server_status
