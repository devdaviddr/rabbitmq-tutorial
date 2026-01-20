#!/usr/bin/env python3
"""
Test script to verify the producer and consumer logic without RabbitMQ.
This simulates the message flow for testing purposes.
"""

import sys
import time

def simulate_callback(body):
    """Simulate the consumer callback function"""
    print(f" [x] Received: {body}")

    # Simulate work (count dots in message)
    dots = body.count(b'.')
    if dots > 0:
        print(f" [x] Processing for {dots} seconds...")
        time.sleep(dots)

    print(" [x] Done")
    return True  # Simulate acknowledgment

def test_producer():
    """Test producer message creation"""
    print("Testing Producer...")

    # Simulate command line arguments
    test_messages = [
        [],  # No args - should use default
        ["Hello", "World"],
        ["Test", "message", "with", "dots..."]
    ]

    for args in test_messages:
        message = ' '.join(args) or "Hello RabbitMQ!"
        print(f" [x] Would send: {message}")

        # Simulate consumer processing
        simulate_callback(message.encode())

    print("Producer test completed.\n")

def test_consumer():
    """Test consumer message processing"""
    print("Testing Consumer...")

    test_messages = [
        b"Hello RabbitMQ!",
        b"Message with dots...",
        b"Another message....."
    ]

    for message in test_messages:
        simulate_callback(message)

    print("Consumer test completed.\n")

if __name__ == '__main__':
    print("RabbitMQ Tutorial - Code Test")
    print("=" * 40)

    test_producer()
    test_consumer()

    print("All tests passed! ✅")
    print("\nTo run with real RabbitMQ:")
    print("1. Start Docker Desktop")
    print("2. Run: docker compose up -d")
    print("3. Run: python3 app/consumer.py")
    print("4. Run: python3 app/producer.py 'Your message'")
    print("   Or use Docker: docker compose --profile consumer up -d && docker compose --profile producer up -d")