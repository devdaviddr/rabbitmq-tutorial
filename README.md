# RabbitMQ Python Tutorial

A practical tutorial demonstrating message queue patterns using RabbitMQ, Docker, and Python. This repository provides working examples of producer-consumer messaging with best practices for reliability and durability.

## Overview

This tutorial covers:

- **RabbitMQ Setup**: Running RabbitMQ with Docker and management UI
- **Python Integration**: Using the `pika` library for AMQP 0-9-1 protocol
- **Message Patterns**: Durable queues, persistent messages, and acknowledgements
- **Best Practices**: Prefetch limits, connection management, and error handling

### What You'll Learn

- Set up RabbitMQ quickly using Docker
- Implement reliable message producers and consumers
- Configure durable queues for message persistence
- Use manual acknowledgements to prevent message loss
- Monitor queues via the RabbitMQ Management UI

### Architecture

```
Producer → [RabbitMQ Queue] → Consumer
   ↓             ↓              ↓
  pika      Docker Image   Message Ack
```

## Quick Start

### Automated Setup (Recommended)

Run the setup script to get everything running:

```bash
./start.sh
```

This will:
- Start RabbitMQ with Docker Compose
- Wait for it to be ready
- Provide connection details and testing options

### Manual Setup

1. **Start RabbitMQ:**
   ```bash
   docker compose up -d
   ```

2. **Choose your testing method:**

   **Option A - Local Python (requires virtual env):**
   ```bash
   # Install dependencies
   pip install -r config/requirements.txt

   # Test messaging
   python3 app/consumer.py    # Terminal 1
   python3 app/producer.py "Hello World!"  # Terminal 2
   ```

   **Option B - Docker containers:**
   ```bash
   # Run producer and consumer as containers
   docker compose --profile producer up -d
   docker compose --profile consumer up -d
   ```

   **Option C - Run test (no RabbitMQ needed):**
   ```bash
   python3 app/test.py
   ```

3. **Monitor via Management UI:**
   - Open: http://localhost:15672
   - Login: `guest` / `guest`

### Project Structure

```
rabbitmq-tutorial/
├── app/                    # Python application code
│   ├── producer.py        # Message producer
│   ├── consumer.py        # Message consumer
│   └── test.py           # Code verification script
├── config/                # Configuration files
│   └── requirements.txt   # Python dependencies
├── docker/                # Docker-related files
│   ├── Dockerfile.producer # Producer container
│   ├── Dockerfile.consumer # Consumer container
│   └── .dockerignore      # Docker build exclusions
├── docker-compose.yml     # Multi-service setup
├── start.sh              # Automated setup script
├── .gitignore           # Git exclusions
└── README.md            # This documentation
```

---

## Prerequisites

- **Docker**: Version 20.10+ with Compose V2 support
- **Python**: 3.8 or higher
- **pip**: Latest version recommended

Verify your environment:

```bash
docker --version
docker compose version
python3 --version
pip3 --version
```

---

## Python Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or create a `requirements.txt`:

```txt
pika==1.3.2
```

Then install:

```bash
pip install -r requirements.txt
```

---

## Implementation

### Producer

Create `producer.py` - sends messages to the queue:

```python
import pika
import sys

def main():
    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()

    # Declare a durable queue (survives broker restart)
    channel.queue_declare(queue='task_queue', durable=True)

    # Prepare message
    message = ' '.join(sys.argv[1:]) or "Hello RabbitMQ!"

    # Publish message with persistence
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,  # Message persistence
        )
    )

    print(f" [x] Sent: {message}")
    connection.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
```

**Key Features:**
- `durable=True`: Queue persists across RabbitMQ restarts
- `delivery_mode=Persistent`: Messages survive broker restart
- Accepts message from command line arguments

### Consumer

Create `consumer.py` - receives and processes messages:

```python
import pika
import time
import sys

def callback(ch, method, properties, body):
    """Process received message"""
    print(f" [x] Received: {body.decode()}")

    # Simulate work (count dots in message)
    time.sleep(body.count(b'.'))

    print(" [x] Done")

    # Send acknowledgment
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Establish connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()

    # Declare queue (idempotent - safe to call multiple times)
    channel.queue_declare(queue='task_queue', durable=True)

    # Fair dispatch - don't give more than one message to a worker at a time
    channel.basic_qos(prefetch_count=1)

    # Set up consumer
    channel.basic_consume(
        queue='task_queue',
        on_message_callback=callback,
        auto_ack=False  # Manual acknowledgment for reliability
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
```

**Key Features:**
- `auto_ack=False`: Manual message acknowledgment (prevents message loss)
- `prefetch_count=1`: Fair distribution across multiple workers
- `basic_ack()`: Confirms message was processed successfully
- Graceful shutdown with CTRL+C

### Running the Examples

**Terminal 1 - Start Consumer:**
```bash
python3 app/consumer.py
```

**Terminal 2 - Send Messages:**
```bash
python3 app/producer.py "First message"
python3 app/producer.py "Second message..."
python3 app/producer.py "Third message....."
```

**Multiple Workers (Terminal 3):**
```bash
# Run another consumer for load distribution
python3 app/consumer.py
```

Messages will be distributed fairly across all running consumers.

---

## Configuration

### Connection Parameters

**Local Development:**
```python
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
```

**Docker Compose Network:**
```python
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq')
)
```

**Custom Configuration:**
```python
import pika
import os

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', 'localhost'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        credentials=pika.PlainCredentials(
            os.getenv('RABBITMQ_USER', 'guest'),
            os.getenv('RABBITMQ_PASS', 'guest')
        ),
        heartbeat=600,
        blocked_connection_timeout=300
    )
)
```

### Environment Variables

Create a `.env` file:

```bash
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASS=guest
```

---

## Monitoring & Debugging

### Management UI Features

Access http://localhost:15672 to:

- **Queues Tab**: View queue depth, message rates, consumers
- **Connections**: Monitor active connections and channels
- **Exchanges**: Inspect routing and bindings
- **Admin**: Manage users, virtual hosts, policies

### Useful Docker Commands

```bash
# View logs
docker logs rabbitmq -f

# Check container status
docker ps | grep rabbitmq

# Restart RabbitMQ
docker restart rabbitmq

# Stop and remove
docker stop rabbitmq && docker rm rabbitmq

# Access RabbitMQ CLI
docker exec -it rabbitmq rabbitmqctl status
```

### Common Issues

**Connection Refused:**
```bash
# Ensure RabbitMQ is running
docker ps | grep rabbitmq

# Check if ports are exposed
netstat -an | grep 5672
```

**Authentication Failed:**
- Default credentials are `guest/guest`
- `guest` user only works from localhost
- For remote access, create a new user via Management UI

**Message Not Persisting:**
- Ensure queue is declared with `durable=True`
- Messages must have `delivery_mode=Persistent`
- Both conditions are required for persistence

---

## Best Practices

### 1. Connection Management
- Reuse connections across multiple channels
- Close connections properly to avoid resource leaks
- Implement reconnection logic for production

### 2. Error Handling
```python
import pika
import time

def get_connection():
    """Get RabbitMQ connection with retry logic"""
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            return pika.BlockingConnection(
                pika.ConnectionParameters('localhost')
            )
        except pika.exceptions.AMQPConnectionError:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise
```

### 3. Message Design
- Use JSON for structured messages
- Include timestamps and correlation IDs
- Keep messages small and atomic

### 4. Monitoring
- Set up alerts for queue depth
- Monitor consumer processing time
- Track message rates and error rates

---

## Advanced Topics

### Work Queues vs Pub/Sub

This tutorial demonstrates **Work Queues** (task distribution). For other patterns:

- **Publish/Subscribe**: Use fanout exchanges
- **Routing**: Use direct exchanges with routing keys
- **Topics**: Use topic exchanges with pattern matching
- **RPC**: Request/Reply pattern with correlation IDs

### Production Considerations

- **Clustering**: Run multiple RabbitMQ nodes for high availability
- **TLS/SSL**: Encrypt connections in production
- **Authentication**: Use proper credentials and virtual hosts
- **Monitoring**: Integrate with Prometheus/Grafana
- **Backup**: Configure persistence and regular backups

---

## Resources

- [RabbitMQ Official Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Pika Documentation](https://pika.readthedocs.io/)
- [AMQP 0-9-1 Protocol](https://www.rabbitmq.com/protocol.html)
- [RabbitMQ Best Practices](https://www.rabbitmq.com/best-practices.html)

---

## Contributing

Contributions are welcome! Areas for improvement:

- Additional messaging patterns (pub/sub, topics, RPC)
- Async examples using `aio-pika`
- Docker multi-container examples
- TLS/SSL configuration
- Production deployment guides
- Monitoring and alerting setup

Feel free to open issues or submit pull requests.

---

## License

MIT License - feel free to use this code for learning and projects.
