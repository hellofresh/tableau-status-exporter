# tableau-status-exporter

Simple Prometheus exporter for monitoring the status of Tableau Server processes.

Please note: Tested **only** with Tableau Server 2018.2 running on a single machine.

## What it does

Reads and parses the /admin/systeminfo.xml page and exports the number of processes with Active, Busy, Passive, Unlicensed, Down and Unknown status for each process group.

## Using the exporter

1. Clone the project
2. Create config file based on config.yml.template. Configs:
    * *tableau_user* and *tableau_password*: credentials for a Tableau Server user with administrative privileges (alternative to token)
    * *tableau_token_name* and *tableau_token_secret*: personal access token for a Tableau Server user with administrative privileges (alternative to user/password)
    * *api_version*: REST API version for the Tableau Server version. See https://onlinehelp.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_versions.htm
    * *server_host*: Tableau Server hostname, starting with http(s)://
    * *site*: The Tableau site to use (if empty, Default site is used)
    * *exporter_port*: Which port to use for the exporter's webserver
    * *log_path* (optional): File to output logs to (if missing or empty, logs go to stdout)
    * *verify_ssl* (optional): Verify SSL request when fetching status from Tableau, defaults to false.
3. Install with `pip install <path_to_project>`. Dependencies:
    * *pyyaml*: YAML config processing
    * *requests*: Accessing the Tableau Server REST API (for login) and the systeminfo.xml page
    * *prometheus_client*: Prometheus python client API
    * *twisted*: Webserver
3. Start the exporter with `python <path_to_project>/executable/main.py --config-file <path_to_config_yml>`
4. Go to `<hostname_of_exporter>:<exporter_port>/metrics` to see the metrics.

Example output:
```
# HELP tableau_server_process_status Process status
# TYPE tableau_server_process_status gauge
tableau_server_process_status{machine="tableau.myhost.com",process="applicationserver",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="applicationserver",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="applicationserver",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="applicationserver",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="applicationserver",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="applicationserver",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="hyper",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="hyper",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="hyper",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="hyper",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="hyper",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="hyper",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="cacheserver",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="cacheserver",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="cacheserver",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="cacheserver",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="cacheserver",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="cacheserver",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="repository",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="repository",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="repository",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="repository",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="repository",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="repository",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="searchandbrowse",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="searchandbrowse",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="searchandbrowse",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="searchandbrowse",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="searchandbrowse",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="searchandbrowse",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="dataserver",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="dataserver",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="dataserver",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="dataserver",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="dataserver",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="dataserver",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="backgrounder",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="backgrounder",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="backgrounder",status="Busy"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="backgrounder",status="Active"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="backgrounder",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="backgrounder",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="clustercontroller",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="clustercontroller",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="clustercontroller",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="clustercontroller",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="clustercontroller",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="clustercontroller",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="filestore",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="filestore",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="filestore",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="filestore",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="filestore",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="filestore",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="vizqlserver",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="vizqlserver",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="vizqlserver",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="vizqlserver",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="vizqlserver",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="vizqlserver",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="coordination",status="Down"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="coordination",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="coordination",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="coordination",status="Active"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="coordination",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="coordination",status="Unlicensed"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="gateway",status="Down"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="gateway",status="Passive"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="gateway",status="Busy"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="gateway",status="Active"} 1.0
tableau_server_process_status{machine="tableau.myhost.com",process="gateway",status="Unknown"} 0.0
tableau_server_process_status{machine="tableau.myhost.com",process="gateway",status="Unlicensed"} 0.0
```

## Contribution Guidelines:

Please feel free to open PRs or create Issues in this repository, we're happy to review or implement them.
