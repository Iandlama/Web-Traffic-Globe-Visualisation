import os
import csv
import json
import time
import requests
from datetime import datetime
from urllib.parse import quote


CSV_FILE = "ip_addresses.csv"

SERVER_URL = os.environ.get('SERVER_URL', 'http://localhost:5000/package')


def send_package(package_data):

    try:

        response = requests.get(
            SERVER_URL,
            params={"data": json.dumps(package_data)},
            timeout=5
        )
        if response.status_code == 200:
            print(
                f"✓ Sent: {package_data['ip']} at {package_data['timestamp']}")
        else:
            print(f"✗ Failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")


def parse_timestamp(ts_str):

    try:
        ts_float = float(ts_str)
        return datetime.fromtimestamp(ts_float)
    except ValueError:
        pass

    try:
        return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
    except:
        pass

    try:
        return datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
    except:
        pass

    raise ValueError(f"Cannot parse timestamp: {ts_str}")


def main():
    packages = []

    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            packages.append({
                'ip': row['ip address'],
                'latitude': float(row['Latitude']),
                'longitude': float(row['Longitude']),
                'timestamp': row['Timestamp'],
                'suspicious': int(float(row['suspicious']))
            })

    packages.sort(key=lambda x: float(x['timestamp']))

    print(f"📦 Loaded {len(packages)} packages")

    prev_time = None

    for pkg in packages:
        current_time = parse_timestamp(pkg['timestamp'])

        if prev_time is not None:

            delta = (current_time - prev_time).total_seconds()
            if delta > 0:
                print(f"⏳ Waiting {delta:.2f} seconds...")
                time.sleep(delta)

        send_package(pkg)
        prev_time = current_time


if __name__ == "__main__":
    print("🚀 Starting data sender...")
    main()
    print("✅ All packages sent!")
