import argparse
import yaml
import logging
from tableau_exporter.tableau_status_exporter import start_webserver


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', required=True)
    args = parser.parse_args()

    with open(args.config_file, "r") as config:
        conf = yaml.load(config)

    if 'log_path' in conf and conf['log_path'] != '':
        logging.basicConfig(filename=conf['log_path'],
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
    else:
        logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    start_webserver(conf)
