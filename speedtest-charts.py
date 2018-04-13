#!/usr/bin/env python3

import os
import subprocess
import re
import datetime
import pygsheets
import speedtest

# Set constants
DATE = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

def get_credentials():
    """Function to check for valid OAuth access tokens."""
    gc = pygsheets.authorize(outh_file="credentials.json", outh_nonlocal=True)
    return gc

def submit_into_spreadsheet(download, upload, ping, sponsor, srv_id):
    """Function to submit speedtest result."""
    gc = get_credentials()

    speedtest = gc.open(os.getenv('SPREADSHEET', 'Speedtest'))
    sheet = speedtest.sheet1

    data = [DATE, download, upload, ping, sponsor, srv_id]

    sheet.append_table(values=data)

def main():
    # Check for proper credentials
    print("Checking OAuth validity...")
    credentials = get_credentials()

    # List of prefered
    servers = [1990,7203,15317,15315]

    # Run speedtest and store output
    print("Starting speed test...")
    spdtest = speedtest.Speedtest()
    spdtest.get_servers(servers)
    spdtest.get_best_server()
    download = spdtest.download()
    upload = spdtest.upload()
    ping = spdtest.results.ping
    server_id = spdtest.results.server.get('id')
    sponsor = spdtest.results.server.get('sponsor')
    print("Starting speed finished!")

    # Write to spreadsheet
    print("Writing to spreadsheet...")
    submit_into_spreadsheet(download, upload, ping, sponsor, server_id)
    print("Successfuly written to spreadsheet!")

if __name__ == "__main__":
    main()
