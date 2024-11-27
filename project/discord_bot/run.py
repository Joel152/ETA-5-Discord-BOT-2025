#!/usr/bin/env python3
import sys
import subprocess
import os

def setup_environment():
    try:
        # Create virtual environment if it doesn't exist
        if not os.path.exists('venv'):
            print("Creating virtual environment...")
            subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)

        # Determine the correct activation script
        if os.name == 'nt':  # Windows
            activate_script = os.path.join('venv', 'Scripts', 'activate')
        else:  # Unix-like
            activate_script = os.path.join('venv', 'bin', 'activate')

        # Install requirements
        if os.name == 'nt':
            pip_cmd = [os.path.join('venv', 'Scripts', 'pip')]
        else:
            pip_cmd = [os.path.join('venv', 'bin', 'pip')]

        print("Installing requirements...")
        subprocess.run([*pip_cmd, 'install', '-r', 'requirements.txt'], check=True)
        
        # Run the bot
        if os.name == 'nt':
            python_cmd = [os.path.join('venv', 'Scripts', 'python')]
        else:
            python_cmd = [os.path.join('venv', 'bin', 'python')]

        print("Starting bot...")
        subprocess.run([*python_cmd, 'bot.py'], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during setup: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_environment()