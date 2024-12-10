import os
from pygbag_builder import make_dir
from pygbag_builder import insert_sleep
from pygbag_builder import insert_await

def main():
    current_directory = os.getcwd()
    make_dir.create_folders_and_files(current_directory)
    insert_sleep.process_files_in_directory(current_directory)
    print(f"To insert await asyncio.sleep(0) in while loop was finished.")
    insert_await.process_files_until_no_change(current_directory)
    print(f"To remake functions into asynchronous functions was finished.")
    
if __name__ == "__main__":
    main()
