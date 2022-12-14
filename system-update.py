#!/usr/bin/env python3

# This script is used to update Depthboot/EupneaOS between releases.

import json
from functions import *

if __name__ == "__main__":
    # Check if running under Depthboot or EupneaOS
    with open("/etc/eupnea.json", "r") as f:
        config = json.load(f)
    try:
        current_version = config["depthboot_version"]
        os_type = "depthboot_version"
        with open("/tmp/eupnea-system-update/configs/depthboot_versions.txt", "r") as f:
            versions_array = f.read().splitlines()
        from depthboot_updates import *  # import the depthboot updates
    except KeyError:
        current_version = config["eupnea_os_version"]
        os_type = "eupnea_os_version"
        # Convert versions.txt into an array
        with open("/tmp/eupnea-system-update/configs/eupnea_os_versions.txt", "r") as f:
            versions_array = f.read().splitlines()
        from eupnea_os_updates import *  # import the EupneaOS updates

    # Remove versions older than current version from the array
    versions_array = versions_array[versions_array.index(current_version) + 1:]

    if len(versions_array) == 0:
        # No updates available.
        exit(0)
    else:
        # Execute update scripts for all versions in the array
        for version in versions_array:
            version = version.replace(".", "_")  # Functions cant have dots in their names -> replace with underscores
            globals()["v" + version]()  # This calls the function named after the version
        # Update version in config with the latest version in the array
        config[os_type] = versions_array[-1]
        with open("/etc/eupnea.json", "w") as file:
            json.dump(config, file)

    # remove the update directory
    rmdir("/tmp/eupnea-system-update", keep_dir=False)
