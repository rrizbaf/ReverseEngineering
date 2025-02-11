What the Script Does

This Python script automates the process of adding new FTD devices to be managed by your FMC, and adds them to the selected domains configured on FMC. It includes robust error handling and logging, making it user-friendly, even for those with minimal programming experience.

Key Components of the Code

Authentication: The script securely authenticates with the FMC using your credentials.

Domain Retrieval: It retrieves the available domains in the FMC and allows you to select the appropriate domain for adding FTD devices.

Device Addition: The script reads the devices to be added from an external configuration file (config.json) and adds them to the selected domain.

Error Handling & Logging: Comprehensive error handling and logging ensure any issues encountered are clearly communicated and recorded for troubleshooting.

How It Works

Setup: Place the script and the config.json file in the same directory.

Configuration File: The config.json file should contain the FMC IP address, username, password, and details of the FTD devices to be added.

Execution: Run the script in your Python environment. It will authenticate with the FMC, retrieve the list of domains, and prompt you to select a domain. It will then add the FTD devices as specified in the configuration file.

Feedback: The script provides real-time feedback and logs detailed information about the process, including any errors encountered. A log file called fmc_add_ftd.log
 gets created to keep track of where you're up to. 

