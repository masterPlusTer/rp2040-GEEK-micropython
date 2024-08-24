
import os

def get_flash_info():
    fs_stat = os.statvfs('/')
    block_size = fs_stat[0]
    total_blocks = fs_stat[1]
    free_blocks = fs_stat[3]

    total_size_bytes = block_size * total_blocks
    free_size_bytes = block_size * free_blocks
    used_size_bytes = total_size_bytes - free_size_bytes

    # Convert bytes to megabytes
    total_size_mb = total_size_bytes / (1024 * 1024)
    free_size_mb = free_size_bytes / (1024 * 1024)
    used_size_mb = used_size_bytes / (1024 * 1024)

    print(f"Total flash size: {total_size_mb:.2f} MB")
    print(f"Free flash space: {free_size_mb:.2f} MB")
    print(f"Used flash space: {used_size_mb:.2f} MB")

# Call the function to get the information
get_flash_info()
