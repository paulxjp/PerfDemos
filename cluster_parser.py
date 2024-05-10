import os
import re

def parse_log(file_path):
    patterns = [
        r'Fence .*',
        r'\[TOTEM \].*',
        r'cib_perform_op',
		r'Node .*is now lost',
		r'node .*not expected',
		r'node is offline',
		r'peer is no longer part of the cluster',
        r'Move rsc',
        r'due to',
        r'SAPHana\(.*\): .*',
        r'HANA_CALL',
        r'status GRAY',
        r'SFAIL',
        r'not.*SOK',
		r'COULD NOT BE PROMOTED',
        r'stonith-ng',
        r'SAPInstance\(.*\): .*',
        r'High CPU load detected: .*',
        r'stonith_notify',
        r'check_migration_threshold',
        r'cib_perform_op: \+\+ /cib/configuration/constraints: .*',
        r'update_cib_stonith_devices',
		r'LogAction',
    ]

    with open(file_path, 'r') as f:
        for line in f:
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    print(line.strip())
                    break  # Break the loop once a match is found

# Ask the user for the file path
file_name = input("Please input the file path: ")
# Get the current script directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# Join the current directory with the user-provided file path
file_path = os.path.join(current_directory, file_name)

parse_log(file_path)
