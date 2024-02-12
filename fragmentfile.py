import os
import random
import time
import hashlib
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define the characters that could be used in the random data
extended_chars = [chr(i) for i in range(32, 127)]

def random_string(chunk_size=1024):
    # Get the current stack frame
    current_frame = sys._getframe()
    # Use the id of the current frame, which is a memory address, as part of the seed
    frame_id = id(current_frame)

    # Combine various elements to create a seed
    seed_elements = [
        frame_id,
        os.urandom(16),  # Cryptographically strong random bytes
        time.time()  # Current time
    ]
    seed = hashlib.md5(b''.join(str(element).encode('utf-8') for element in seed_elements)).hexdigest()

    # Generate a random string based on the complex seed
    random.seed(seed)
    random_str = ''.join(random.choice(extended_chars) for _ in range(chunk_size))

    # Reset the random seed if necessary for other parts of the application
    random.seed()

    return random_str

def create_file(filename, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb):
    print(f"{filename} creation start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with open(filename, 'wb') as f:
        target_size = target_size_mb * 1024 * 1024  # Convert MB to bytes
        current_size = 0
        while current_size < target_size:
            # Determine the size of the next chunk
            chunk_size = random.randint(min_chunk_kb, max_chunk_kb) * 1024  # Convert KB to bytes

            # Write a random string of data of the determined size
            f.write(random_string(chunk_size).encode('utf-8'))
            current_size += chunk_size

            # Optionally seek to a random position within the file to create a gap
            if offset_kb > 0:
                offset = random.randint(0, offset_kb) * 1024  # Convert KB to bytes
                f.seek(offset, os.SEEK_CUR)
                current_size += offset

    print(f"{filename} creation finish time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    os.sync()

def delete_file(filename):
    print(f"{filename} deletion start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")
    except OSError as e:
        print(f"Error: {e.strerror}")
    print(f"{filename} deletion finish time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    os.sync()

def create_and_delete_file(file_number, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb):
    filename = f'fragmented_file_{file_number}.bin'
    create_file(filename, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb)
    delete_file(filename)

def main(N, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb):
    with ThreadPoolExecutor(max_workers=N) as executor:
        futures = [executor.submit(create_and_delete_file, i, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb) for i in range(N)]
        for future in as_completed(futures):
            future.result()  # Wait for each thread to complete its task

if __name__ == "__main__":
    # Adjust the parameters as needed:
    N = 10  # Number of files to create and delete
    target_size_mb = 100  # Size of each file in megabytes
    min_chunk_kb = 4  # Minimum chunk size in kilobytes
    max_chunk_kb = 16  # Maximum chunk size in kilobytes
    offset_kb = 4  # Maximum offset for fragmentation in kilobytes
    main(N, target_size_mb, min_chunk_kb, max_chunk_kb, offset_kb)
