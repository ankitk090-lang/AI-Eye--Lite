#!/usr/bin/env python3
"""
Test script for the AI-Eye Watcher Agent
Tests the core functionality without running the full scheduled loop.
"""

import sys
import time
import subprocess
import requests
from agent import collect_system_data, execute_kill_process, CENTRAL_SERVER_URL, AGENT_HOSTNAME

def test_data_collection():
    """Test system data collection."""
    print("Testing data collection...")
    data = collect_system_data()
    
    print(f"Hostname: {data['hostname']}")
    print(f"Processes collected: {len(data['processes'])}")
    print(f"Connections collected: {len(data['connections'])}")
    print(f"System info keys: {list(data['system_info'].keys())}")
    
    # Show a few sample processes
    print("\nSample processes:")
    for i, proc in enumerate(data['processes'][:3]):
        print(f"  {i+1}. PID {proc['pid']}: {proc['name']} (User: {proc['user']})")
    
    return data

def test_server_connection():
    """Test connection to Central Server."""
    print(f"\nTesting connection to Central Server at {CENTRAL_SERVER_URL}...")
    
    try:
        response = requests.get(f"{CENTRAL_SERVER_URL}/health", timeout=5)
        response.raise_for_status()
        print("✓ Central Server is reachable")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot reach Central Server: {e}")
        return False

def test_telemetry_send():
    """Test sending telemetry to Central Server."""
    print("\nTesting telemetry transmission...")
    
    data = collect_system_data()
    
    try:
        response = requests.post(
            f"{CENTRAL_SERVER_URL}/api/v1/collect",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        print(f"✓ Telemetry sent successfully: {result}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to send telemetry: {e}")
        return False

def test_command_polling():
    """Test command polling from Central Server."""
    print("\nTesting command polling...")
    
    try:
        response = requests.get(
            f"{CENTRAL_SERVER_URL}/api/v1/commands",
            params={"host": AGENT_HOSTNAME},
            timeout=10
        )
        response.raise_for_status()
        commands = response.json()
        print(f"✓ Command polling successful. Received {len(commands)} commands")
        
        if commands:
            print("Commands received:")
            for cmd in commands:
                print(f"  - {cmd.get('action')} on {cmd.get('target')}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to poll commands: {e}")
        return False

def test_kill_process():
    """Test process killing functionality with a test process."""
    print("\nTesting process killing functionality...")
    
    # Start a test process (sleep)
    print("Starting test process (sleep 30)...")
    proc = subprocess.Popen(['sleep', '30'])
    test_pid = proc.pid
    print(f"Test process PID: {test_pid}")
    
    # Wait a moment
    time.sleep(1)
    
    # Test killing the process
    print(f"Attempting to kill test process {test_pid}...")
    success = execute_kill_process(str(test_pid))
    
    if success:
        print("✓ Process killing test successful")
    else:
        print("✗ Process killing test failed")
        # Clean up if the test failed
        try:
            proc.terminate()
        except:
            pass
    
    return success

def main():
    """Run all tests."""
    print("AI-Eye Watcher Agent Test Suite")
    print("=" * 40)
    
    tests = [
        ("Data Collection", test_data_collection),
        ("Server Connection", test_server_connection),
        ("Telemetry Send", test_telemetry_send),
        ("Command Polling", test_command_polling),
        ("Process Killing", test_kill_process)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 40)
    print("TEST SUMMARY")
    print("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The agent is ready to run.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        if not results.get("Server Connection", False):
            print("\nMake sure the Central Server is running:")
            print("cd ai-eye-watcher-backend && python3 central_server.py")

if __name__ == "__main__":
    main()