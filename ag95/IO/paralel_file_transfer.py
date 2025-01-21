import os
import shutil
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Function to copy chunks in parallel
def _copy_chunk(source_path, dest_path,
               start, end,
               chunk_size=1024 * 1024,
               max_speed_bytes_s=None,
               fragment_id=None,
               total_size=None,
               lock=None):

    with (open(source_path, 'rb') as src,
          open(dest_path, 'r+b') as dest):
        src.seek(start)
        dest.seek(start)

        start_time = time.time()  # To track the time for rate limiting
        bytes_transferred = 0
        last_update_time = time.time()
        total_bytes_transferred = 0

        while start < end:
            chunk = src.read(chunk_size)
            if not chunk:
                break
            dest.write(chunk)
            bytes_transferred += len(chunk)
            total_bytes_transferred += len(chunk)
            start += len(chunk)

            # Check transfer rate and enforce speed limit
            if max_speed_bytes_s:
                elapsed_time = time.time() - start_time
                current_rate = bytes_transferred / elapsed_time
                if current_rate > max_speed_bytes_s:
                    # Calculate how much time to sleep to enforce the speed limit
                    sleep_time = (bytes_transferred / max_speed_bytes_s) - elapsed_time
                    if sleep_time > 0:
                        time.sleep(sleep_time)

            # Update progress every second
            if time.time() - last_update_time > 1:  # Update every second
                last_update_time = time.time()
                progress = (total_bytes_transferred / total_size) * 100
                with lock:  # Ensure that the printing is synchronized
                    print(f"Fragment {fragment_id}: [{'-' * int(progress // 2):<50}] {progress:.2f}%")

        # Final update after completing the chunk
        progress = (total_bytes_transferred / total_size) * 100
        with lock:  # Ensure that the final print is synchronized
            print(f"Fragment {fragment_id}: [{'-' * int(progress // 2):<50}] {progress:.2f}% - Done!")


def single_file_transfer(source_path, destination_path, num_threads=4, max_speed_mb_s=None):
    # Convert max speed from MB/s to bytes per second
    max_speed_bytes_s = max_speed_mb_s * 1024 * 1024 if max_speed_mb_s else None

    # Get source file size
    source_size = os.path.getsize(source_path)

    # Prepare the destination file
    destination_file = destination_path + ".part"

    # Divide file into chunks
    chunk_size = source_size // num_threads
    lock = threading.Lock()  # Create a lock for synchronized printing
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for i in range(num_threads):
            start = i * chunk_size
            end = (i + 1) * chunk_size if i < num_threads - 1 else source_size
            futures.append(
                executor.submit(_copy_chunk,
                                source_path, destination_file,
                                start, end,
                                1024 * 1024,
                                max_speed_bytes_s,
                                i + 1,
                                source_size,
                                lock))

        # Wait for all threads to complete
        for future in futures:
            future.result()

    # Replace the original file with the completed temporary file
    os.rename(destination_file, destination_path)
    with lock:  # Final completion message, synchronized
        print("\nFile transfer completed with parallel chunks.")

    os.remove(source_path)  # Remove the source file after copying

if __name__ == '__main__':
    source_path = r"<some_input_filepath>"
    destination_path = r"<some_output_filepath>"
    max_speed = 2
    single_file_transfer(source_path,
                         destination_path,
                         num_threads=4,
                         # max_speed_mb_s=max_speed
                         )

    print('MANUAL assessment required !')
