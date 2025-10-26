#!/usr/bin/env python3
"""
Test script for AI-Eye Watcher Central Server
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:9000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_collect_normal_telemetry():
    """Test normal telemetry collection"""
    print("\nTesting normal telemetry collection...")
    
    payload = {
        "hostname": "test-host-01",
        "timestamp": datetime.now().isoformat(),
        "processes": [
            {
                "pid": 1234,
                "name": "chrome",
                "command_line": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "user": "testuser",
                "cpu_percent": 5.2,
                "memory_percent": 12.1
            },
            {
                "pid": 5678,
                "name": "python3",
                "command_line": "python3 central_server.py",
                "user": "testuser",
                "cpu_percent": 1.0,
                "memory_percent": 3.5
            }
        ],
        "connections": [
            {
                "local_address": "127.0.0.1",
                "local_port": 9000,
                "remote_address": "0.0.0.0",
                "remote_port": 0,
                "status": "LISTEN",
                "pid": 5678
            }
        ],
        "system_info": {
            "os": "macOS",
            "version": "14.0"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/collect", json=payload)
    print(f"Normal telemetry: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_collect_malicious_telemetry():
    """Test telemetry with known bad process"""
    print("\nTesting malicious telemetry collection...")
    
    payload = {
        "hostname": "test-host-02",
        "timestamp": datetime.now().isoformat(),
        "processes": [
            {
                "pid": 9999,
                "name": "nc.exe",  # Known bad process
                "command_line": "nc.exe -l -p 4444",
                "user": "attacker",
                "cpu_percent": 0.1,
                "memory_percent": 0.5
            },
            {
                "pid": 8888,
                "name": "mimikatz.exe",  # Another known bad process
                "command_line": "mimikatz.exe sekurlsa::logonpasswords",
                "user": "attacker",
                "cpu_percent": 2.0,
                "memory_percent": 1.2
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/collect", json=payload)
    print(f"Malicious telemetry: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_dashboard_stats():
    """Test dashboard stats endpoint"""
    print("\nTesting dashboard stats...")
    
    response = requests.get(f"{BASE_URL}/api/v1/dashboard/stats")
    print(f"Dashboard stats: {response.status_code}")
    if response.status_code == 200:
        stats = response.json()
        print(f"  Events: {stats['event_count']}")
        print(f"  Alerts: {stats['alert_count']}")
        print(f"  Unique hosts: {stats['unique_hosts']}")
        print(f"  Alert breakdown: {stats['alert_severity_breakdown']}")
    return response.status_code == 200

def test_alerts():
    """Test alerts endpoint"""
    print("\nTesting alerts endpoint...")
    
    response = requests.get(f"{BASE_URL}/api/v1/alerts")
    print(f"Alerts: {response.status_code}")
    if response.status_code == 200:
        alerts = response.json()
        print(f"  Found {len(alerts)} alerts")
        for alert in alerts[:3]:  # Show first 3 alerts
            print(f"    - {alert['severity']}: {alert['details']}")
    return response.status_code == 200

def test_commands():
    """Test commands endpoint"""
    print("\nTesting commands endpoint...")
    
    # Test for host with malicious processes
    response = requests.get(f"{BASE_URL}/api/v1/commands?host=test-host-02")
    print(f"Commands for test-host-02: {response.status_code}")
    if response.status_code == 200:
        commands = response.json()
        print(f"  Found {len(commands)} commands")
        for cmd in commands:
            print(f"    - {cmd['action']} target: {cmd['target']}")
    
    # Test again (should be empty now)
    response = requests.get(f"{BASE_URL}/api/v1/commands?host=test-host-02")
    print(f"Commands for test-host-02 (second call): {response.status_code}")
    if response.status_code == 200:
        commands = response.json()
        print(f"  Found {len(commands)} commands (should be 0)")
    
    return True

def main():
    """Run all tests"""
    print("AI-Eye Watcher Central Server Test Suite")
    print("=" * 50)
    
    tests = [
        test_health,
        test_collect_normal_telemetry,
        test_collect_malicious_telemetry,
        test_dashboard_stats,
        test_alerts,
        test_commands
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. Check server is running on port 9000.")

if __name__ == "__main__":
    main()