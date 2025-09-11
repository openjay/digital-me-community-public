#!/bin/bash

# Test script for Digital Me Community endpoints
# This avoids shell quote issues by using a script

echo "=== Digital Me Community - Endpoint Tests ==="
echo

# Test health endpoint
echo "1. Testing Health Endpoint..."
curl -s http://localhost:8080/health | python3 -m json.tool
echo
echo

# Test greeting endpoint
echo "2. Testing Greeting Endpoint..."
curl -s -X POST "http://localhost:8080/greet?name=Investor" | python3 -m json.tool
echo
echo

# Test echo endpoint
echo "3. Testing Echo Endpoint..."
curl -s -X POST "http://localhost:8080/echo?message=Hello%20Digital%20Me%20Community" | python3 -m json.tool
echo
echo

# Test stats endpoint
echo "4. Testing Stats Endpoint..."
curl -s http://localhost:8080/stats | python3 -m json.tool
echo
echo

# Test metrics endpoint
echo "5. Testing Metrics Endpoint..."
curl -s http://localhost:8080/metrics
echo
echo

echo "=== All Tests Complete ==="
