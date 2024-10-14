# Building Documentation Locally


def main():
    print("Step 1: Install Python and Required Packages")
    print("Update the package list and install Python 3.10 and its development tools:")
    print("```bash")
    print("sudo apt update")
    print("sudo apt install python3.10 python3.10-venv python3.10-dev")
    print("```")

    print("\nStep 2: Navigate to the Package Root")
    print("Go to the root directory of your project:")
    print("```bash")
    print("cd ~/framecat")
    print("```")

    print("\nStep 3: Create a Virtual Environment")
    print("Create a virtual environment named `.docs_venv`:")
    print("```bash")
    print("python3 -m venv .docs_venv")
    print("source .docs_venv/bin/activate")
    print("```")

    print("\nStep 4: Install Documentation Dependencies")
    print("Install the necessary documentation dependencies:")
    print("```bash")
    print("pip install uv")
    print("pip install -e .[docs]")
    print("```")

    print("\nStep 5: Build the Documentation")
    print("Build the documentation using Sphinx:")
    print("```bash")
    print("sphinx-build docs docs/_build --keep-going")
    print("```")
    print("To fail the build when there is a warning, you can add the `-W` flag:")
    print("```bash")
    print("sphinx-build docs docs/_build -W --keep-going")
    print("```")

    print("\nStep 6: Serve the Documentation Locally")
    print("Serve the built documentation on a local server:")
    print("```bash")
    print("python3 -m http.server --directory docs/_build 8002")
    print("```")

    print("\nStep 7: Clean Up Built Documentation")
    print("To clean up the built documentation, run:")
    print("```bash")
    print("rm -rf docs/_build")
    print("```")


main()
