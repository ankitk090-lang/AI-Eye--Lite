#!/bin/bash

# AI-Eye Watcher Central Server - Manual Testing Script
# Run this script to test the server endpoints manually

BASE_URL="http://localhost:9000"

echo "AI-Eye Watcher Central Server - Manual Tests"
echo "============================================="

echo -e "\n1. Health Check:"
curl -s "$BASE_URL/health" | python3 -m json.tool

echo -e "\n2. Send Normal Telemetry:"
curl -s -X POST "$BASE_URL/api/v1/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "test-host-01",
    "timestamp": "2024-01-01T12:00:00",
    "processes": [
      {
        "pid": 1234,
        "name": "chrome",
        "command_line": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "user": "testuser",
        "cpu_percent": 5.2,
        "memory_percent": 12.1
      }
    ],
    "connections": [
      {
        "local_address": "127.0.0.1",
        "local_port": 9000,
        "status": "LISTEN",
        "pid": 1234
      }
    ]
  }' | python3 -m json.tool

echo -e "\n3. Send Malicious Telemetry (nc.exe):"
curl -s -X POST "$BASE_URL/api/v1/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "compromised-host",
    "timestamp": "2024-01-01T12:05:00",
    "processes": [
      {
        "pid": 9999,
        "name": "nc.exe",
        "command_line": "nc.exe -l -p 4444",
        "user": "attacker",
        "cpu_percent": 0.1,
        "memory_percent": 0.5
      }
    ]
  }' | python3 -m json.tool

echo -e "\n4. Send Malicious Telemetry (mimikatz.exe):"
curl -s -X POST "$BASE_URL/api/v1/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "compromised-host",
    "timestamp": "2024-01-01T12:10:00",
    "processes": [
      {
        "pid": 8888,
        "name": "mimikatz.exe",
        "command_line": "mimikatz.exe sekurlsa::logonpasswords",
        "user": "attacker",
        "cpu_percent": 2.0,
        "memory_percent": 1.2
      }
    ]
  }' | python3 -m json.tool

echo -e "\n5. Check Dashboard Stats:"
curl -s "$BASE_URL/api/v1/dashboard/stats" | python3 -m json.tool

echo -e "\n6. Check Alerts:"
curl -s "$BASE_URL/api/v1/alerts" | python3 -m json.tool

echo -e "\n7. Check Commands for compromised-host:"
curl -s "$BASE_URL/api/v1/commands?host=compromised-host" | python3 -m json.tool

echo -e "\n8. Check Commands Again (should be empty):"
curl -s "$BASE_URL/api/v1/commands?host=compromised-host" | python3 -m json.tool

echo -e "\n9. Check Recent Events:"
curl -s "$BASE_URL/api/v1/events?limit=5" | python3 -m json.tool

echo -e "\nTesting complete!"
echo "Visit http://localhost:9000/docs for interactive API documentation"