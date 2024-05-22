import os
import re
import sys
from datetime import datetime

def parse_log(file_path, output_file=None):
    patterns = [
        r'Fence .*',
        r'maintenance-mode',
        r'\[TOTEM \].*',
        r'cib_perform_op',
        r'pcmk_shutdown_worker',
        r'Node .*is now lost',
        r'node .*not expected',
        r'node is offline',
        r'peer is no longer part of the cluster',
		r'unresponsive to ipc',
        r'Move rsc',
        r'due to',
        r'SAPHana\(.*\): .*',
        r'HANA_CALL',
        r'status GRAY',
        r'SFAIL',
        r'not.*SOK',
        r'COULD NOT BE PROMOTED',
		r'promote',
		r'demote',
        r'stonith-ng',
        r'SAPInstance\(.*\): .*',
        r'High CPU load detected: .*',
        r'stonith_notify',
        r'check_migration_threshold',
        r'cib_perform_op: \+\+ /cib/configuration/constraints: .*',
        r'update_cib_stonith_devices',
        r'LogAction',
        r'CrowdStrike',
        r'ds_agent',
        r'Timed Out after'
    ]

    # If the user just pressed enter without providing a file name, return early
    if not file_path:
        return

    try:
        with open(file_path, 'r') as f:
            for line in f:
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        if output_file:
                            output_file.write(line.strip() + '\n')
                        else:
                            print(line.strip())
                        break  # Break the loop once a match is found
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

# Ask the user for the file paths
file_name1 = input("Please input the first file path: ")
file_name2 = input("Please input the second file path (press enter to skip): ")

# Get the current script directory
current_directory = os.path.dirname(os.path.realpath(__file__))
# Join the current directory with the user-provided file paths
file_path1 = os.path.join(current_directory, file_name1)
file_path2 = os.path.join(current_directory, file_name2) if file_name2 else None

# Check if the files exist before proceeding
if not os.path.isfile(file_path1) or (file_path2 and not os.path.isfile(file_path2)):
    print("One or both of the provided files do not exist.")
    sys.exit(1)

# Ask the user if they want to save the output to a file
save_output = input("Do you want to save the output to a file? (y/n): ").lower()

output_file = None
if save_output in ['y', 'yes']:
    timestamp = datetime.now().strftime('%m-%d-%H%M%S')
    output_file_name = f'logparser{timestamp}.txt'
    output_file = open(output_file_name, 'w')

parse_log(file_path1, output_file)
if file_path2:  # Only parse the second file if a name was provided
    parse_log(file_path2, output_file)

if output_file:
    output_file.close()
    print(f"Output saved to file: {output_file_name}")
