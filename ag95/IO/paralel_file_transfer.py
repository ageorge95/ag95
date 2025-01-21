import os
import time
import threading
import pickle
import traceback
from concurrent.futures import ThreadPoolExecutor

# Function to save progress in a thread-safe manner
def _save_progress(progress_filename, thread_id, position_b, lock):
    '''
    NOTE for future self: This function was designed in this way to allow each thread to
    save its progress without needing to know the progress of the other threads
    '''
    with lock:  # Acquire the lock before writing to the file
        with open(progress_filename, 'ab') as f:
            pickle.dump((thread_id, position_b), f)

# Function to load progress
def _load_progress(progress_filename, num_threads):
    '''
    NOTE for future self: This function was designed in this way to allow each thread to
    save its progress without needing to know the progress of the other threads
    '''
    print('Loading last saved progress ...')
    progress = {i: 0 for i in range(num_threads)}  # Initialize progress dictionary for each chunk
    if os.path.exists(progress_filename):
        with open(progress_filename, 'rb') as f:
            while True:
                try:
                    thread_id, position_b = pickle.load(f)
                    progress[thread_id] = position_b
                except EOFError:
                    break
    print(f'Loaded progress: {progress}')
    return progress

# Function to copy chunks in parallel
def _copy_chunk(source_filepath, dest_filepath,
                start_position_b, end_position_b,
                progress_print_lock,
                progress_dump_lock,
                chunk_size_b=1024 * 1024,
                max_speed_bytes_s=None,
                thread_id=None,
                total_size_b=None,
                progress_filename=None):

    with progress_print_lock:
        print(f"Thread {thread_id} starting at position[bytes] {start_position_b}...")

    with (open(source_filepath, 'rb') as src,
          open(dest_filepath, ('r+b' if os.path.isfile(dest_filepath) else 'w+b')) as dest):

        src.seek(start_position_b)
        dest.seek(start_position_b)

        with progress_print_lock:
            print(f"Thread {thread_id} started successfully")

        bytes_transferred = 0
        start_time = time.time()  # To track the time for rate limiting

        # thread safe locks
        last_progress_print_time = time.time()
        last_progress_dump_time = time.time()

        while start_position_b < end_position_b:
            file_chunk = src.read(chunk_size_b)
            if not file_chunk:
                break
            dest.write(file_chunk)
            bytes_transferred += len(file_chunk)
            start_position_b += len(file_chunk)

            # Check transfer rate and enforce speed limit
            if max_speed_bytes_s:
                elapsed_time = time.time() - start_time
                current_rate = bytes_transferred / elapsed_time
                if current_rate > max_speed_bytes_s:
                    sleep_time = (bytes_transferred / max_speed_bytes_s) - elapsed_time
                    if sleep_time > 0:
                        time.sleep(sleep_time)

            # Print progress every second
            if time.time() - last_progress_print_time > 1:
                last_progress_print_time = time.time()
                progress_percent = ((bytes_transferred) / total_size_b) * 100
                with progress_print_lock:
                    print(f"Thread {thread_id} - [{'-' * int(progress_percent // 2):<50}] {progress_percent:.2f}%")

            # Dump progress every 10 seconds
            if progress_filename and time.time() - last_progress_dump_time > 10:
                last_progress_dump_time = time.time()
                _save_progress(progress_filename, thread_id, bytes_transferred, progress_dump_lock)

        progress_percent = 100
        with progress_print_lock:
            print(f"Thread {thread_id} - [{'-' * int(progress_percent // 2):<50}] {progress_percent:.2f}% - Done!")

def single_file_transfer(source_filepath, destination_filepath,
                         num_threads=4,
                         max_speed_mb_s=None,
                         move=False,
                         progress_filename='transfer_progress.pkl'):

    if not os.path.isfile(destination_filepath):

        max_speed_bytes_s = max_speed_mb_s * 1024 * 1024 if max_speed_mb_s else None

        source_size_b = os.path.getsize(source_filepath)

        # Prepare the destination file
        temp_destination_filepath = destination_filepath + ".part"

        chunk_size_b = source_size_b // num_threads
        progress_print_lock = threading.Lock()  # Create a lock for synchronized printing
        progress_dump_lock = threading.Lock()  # Create a lock for synchronized printing

        print(f'Starting the thread pool for a file with size[bytes] {source_size_b}'
              f' and a chunk size[bytes] of {chunk_size_b}'
              f' allocated to each of the {num_threads} threads.')

        # Load saved progress, if any
        previous_progress = _load_progress(progress_filename, num_threads)

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(num_threads):
                start_position_b = (i * chunk_size_b) + previous_progress[i]
                end_position_b = (i + 1) * chunk_size_b if i < num_threads - 1 else source_size_b

                with progress_print_lock:
                    print(f"Starting thread {i} with range[bytes] "
                          f"({start_position_b} (progress {previous_progress[i]}), {end_position_b})")

                futures.append(
                    executor.submit(_copy_chunk,
                                    source_filepath, temp_destination_filepath,
                                    start_position_b, end_position_b,
                                    progress_print_lock,
                                    progress_dump_lock,
                                    1024 * 1024,
                                    max_speed_bytes_s,
                                    i,
                                    end_position_b - start_position_b,
                                    progress_filename))

            # Wait for all threads to complete
            for future in futures:
                try:
                    future.result()  # This will raise an exception if the thread raised one
                except Exception as e:
                    print(f"Error occurred in thread: {traceback.format_exc(chain=False)}")
                    raise

        # Replace the original file with the completed temporary file
        os.rename(temp_destination_filepath, destination_filepath)
        print("\nFile transfer completed with parallel chunks.")

        if move:
            os.remove(source_filepath)  # Remove the source file after copying

        # remove the progress file, as the file was copied successfully
        os.remove(progress_filename)  # Remove the source file after copying

    else:
        print(f'!! File ({destination_filepath}) already copied; No action taken !!!')

if __name__ == '__main__':
    source_path = r"<some_input_filepath>"
    destination_path = r"<some_output_filepath>"
    max_speed = 2
    single_file_transfer(source_path,
                         destination_path,
                         num_threads=4,
                         # max_speed_mb_s=max_speed,
                         # move=True
                         )

    print('MANUAL assessment required !')
