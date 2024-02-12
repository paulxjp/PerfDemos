import os
import random
import hashlib
import time
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the characters that could be used in the random data
extended_chars = [chr(i) for i in range(32, 127)]

def get_system_uptime():
    # Read the uptime in seconds from the first field of /proc/uptime
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds

def random_string(chunk_size=1024):
    # Generate a random string of specified chunk size
    # This uses a combination of the current frame ID, os.urandom, and the curre                                                                                                                                                       nt time to seed the random generator
    # for a unique random sequence each time
    current_frame = sys._getframe()
    frame_id = id(current_frame)

    seed_elements = [
        frame_id,
        os.urandom(16),
        time.time()
    ]
    seed = hashlib.md5(b''.join(str(element).encode('utf-8') for element in seed                                                                                                                                                       _elements)).hexdigest()
    random.seed(seed)
    random_str = ''.join(random.choice(extended_chars) for _ in range(chunk_size                                                                                                                                                       ))
    random.seed()  # Reset the random seed to its original state
    return random_str

def create_file(filename, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb)                                                                                                                                                       :
    # Create a file with random data
    # This function writes chunks of random data to a file until it reaches the                                                                                                                                                        target size
    # It can also seek a random offset after each chunk if offset_kb is greater                                                                                                                                                        than 0
    print(f"{filename} creation start time: {datetime.now().strftime('%Y-%m-%d %                                                                                                                                                       H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    with open(filename, 'wb') as f:
        target_size = target_size_mb * 1024 * 1024  # Calculate the target size                                                                                                                                                        in bytes
        current_size = 0
        while current_size < target_size:
            chunk_size = random.randint(min_chunk_kb, max_chunk_kb) * 1024  # De                                                                                                                                                       termine the size of the next chunk
            f.write(random_string(chunk_size).encode('utf-8'))  # Write the rand                                                                                                                                                       om string to the file
            current_size += chunk_size
            if offset_kb > 0:
                offset = random.randint(0, offset_kb) * 1024  # Calculate a rand                                                                                                                                                       om offset
                f.seek(offset, os.SEEK_CUR)  # Seek to the new file position
                current_size += offset
    print(f"{filename} creation finish time: {datetime.now().strftime('%Y-%m-%d                                                                                                                                                        %H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    os.sync()  # Flush the file system buffers

def delete_file(filename):
    # Delete the specified file and print the start and finish times with system                                                                                                                                                        uptime
    print(f"{filename} deletion start time: {datetime.now().strftime('%Y-%m-%d %                                                                                                                                                       H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    try:
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")
    except OSError as e:
        print(f"Error: {e.strerror}")
    print(f"{filename} deletion finish time: {datetime.now().strftime('%Y-%m-%d                                                                                                                                                        %H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    os.sync()

def create_and_delete_file(file_number, target_size_mb, min_chunk_kb, max_chunk_                                                                                                                                                       kb, offset_kb):
    # Wrapper function to create and then delete a file
    filename = f'fragmented_file_{file_number}.bin'
    create_file(filename, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb)
    delete_file(filename)

def main(N, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb):
    # Main function to execute file creation and deletion in parallel using a th                                                                                                                                                       read pool
    with ThreadPoolExecutor(max_workers=N) as executor:
        futures = [executor.submit(create_and_delete_file, i, target_size_mb, mi                                                                                                                                                       n_chunk_kb, max_chunk_kb, offset_kb) for i in range(N)]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    # Example usage: create and delete 5 files of 1 MB size with random data
    N = 10  # Number of files
    target_size_mb = 50  # Target file size in MB
    min_chunk_kb = 4  # Minimum chunk size in KB for file creation
    max_chunk_kb = 16  # Maximum chunk size in KB for file creation
    offset_kb = 4  # Random offset in KB after writing each chunk

    main(N, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb)

[root@vm-RH86 data1]# cat fragmentfile.py
import os
import random
import hashlib
import time
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the characters that could be used in the random data
extended_chars = [chr(i) for i in range(32, 127)]

def get_system_uptime():
    # Read the uptime in seconds from the first field of /proc/uptime
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds

def random_string(chunk_size=1024):
    # Generate a random string of specified chunk size
    # This uses a combination of the current frame ID, os.urandom, and the current time to seed the random generator
    # for a unique random sequence each time
    current_frame = sys._getframe()
    frame_id = id(current_frame)

    seed_elements = [
        frame_id,
        os.urandom(16),
        time.time()
    ]
    seed = hashlib.md5(b''.join(str(element).encode('utf-8') for element in seed_elements)).hexdigest()
    random.seed(seed)
    random_str = ''.join(random.choice(extended_chars) for _ in range(chunk_size))
    random.seed()  # Reset the random seed to its original state
    return random_str

def create_file(filename, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb):
    # Create a file with random data
    # This function writes chunks of random data to a file until it reaches the target size
    # It can also seek a random offset after each chunk if offset_kb is greater than 0
    print(f"{filename} creation start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    with open(filename, 'wb') as f:
        target_size = target_size_mb * 1024 * 1024  # Calculate the target size in bytes
        current_size = 0
        while current_size < target_size:
            chunk_size = random.randint(min_chunk_kb, max_chunk_kb) * 1024  # Determine the size of the next chunk
            f.write(random_string(chunk_size).encode('utf-8'))  # Write the random string to the file
            current_size += chunk_size
            if offset_kb > 0:
                offset = random.randint(0, offset_kb) * 1024  # Calculate a random offset
                f.seek(offset, os.SEEK_CUR)  # Seek to the new file position
                current_size += offset
    print(f"{filename} creation finish time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    os.sync()  # Flush the file system buffers

def delete_file(filename):
    # Delete the specified file and print the start and finish times with system uptime
    print(f"{filename} deletion start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    try:
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")
    except OSError as e:
        print(f"Error: {e.strerror}")
    print(f"{filename} deletion finish time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Uptime: {get_system_uptime()} seconds)")
    os.sync()

def create_and_delete_file(file_number, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb):
    # Wrapper function to create and then delete a file
    filename = f'fragmented_file_{file_number}.bin'
    create_file(filename, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb)
    delete_file(filename)

def main(N, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb):
    # Main function to execute file creation and deletion in parallel using a thread pool
    with ThreadPoolExecutor(max_workers=N) as executor:
        futures = [executor.submit(create_and_delete_file, i, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb) for i in range(N)]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    # Example usage: create and delete 5 files of 1 MB size with random data
    N = 10  # Number of files
    target_size_mb = 50  # Target file size in MB
    min_chunk_kb = 4  # Minimum chunk size in KB for file creation
    max_chunk_kb = 16  # Maximum chunk size in KB for file creation
    offset_kb = 4  # Random offset in KB after writing each chunk

    main(N, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb)
