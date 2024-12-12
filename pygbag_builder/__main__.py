import sys
from pygbag_builder.main_flow import main as main_flow
from pygbag_builder.make_repo import main as make_repo
from pygbag_builder.set_page import main as set_page
def main():
    if len(sys.argv) < 2:
        print("Usage: python -m pygbag_builder <command>")
        print("Available commands: main_flow, make_repo, set_page")
        return
    command = sys.argv[1]
    if command == "main_flow":
        main_flow()
    elif command == "make_repo":
        make_repo()
    elif command == "set_page":
        set_page()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: main_flow, make_repo, set_page")
if __name__ == "__main__":
    main()