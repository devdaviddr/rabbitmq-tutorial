# RabbitMQ Python Tutorial

A simple demonstration of message queuing with RabbitMQ, Docker, and Python. This project shows how to send and receive messages using a producer-consumer pattern with containerized services.

## What This Does

This project demonstrates:
- **Producer**: Sends messages to a RabbitMQ queue
- **Consumer**: Receives and processes messages from the queue
- **RabbitMQ**: Message broker that manages the queue
- **Docker**: Everything runs in containers for easy setup

## Quick Start

### Option 1: Run Everything Together (Simplest)

Start all services (RabbitMQ + Producer + Consumer):

```bash
docker compose -f docker-compose.full.yml up -d
```

Check the logs to see messages being sent and received:

```bash
docker compose -f docker-compose.full.yml logs -f
```

Stop everything:

```bash
docker compose -f docker-compose.full.yml down
```

### Option 2: Run Services Separately (More Control)

Start just RabbitMQ:

```bash
docker compose up -d
```

Add the producer:

```bash
docker compose --profile producer up -d
```

Add the consumer:

```bash
docker compose --profile consumer up -d
```

Check logs:

```bash
docker compose logs -f
```

Stop everything:

```bash
docker compose down
```

## Viewing Messages in Real-Time

To see messages being consumed as they arrive:

```bash
# Stop the background consumer
docker compose -f docker-compose.full.yml stop consumer

# Run consumer in foreground (Terminal 1)
docker compose -f docker-compose.full.yml exec consumer python consumer.py

# Send a message (Terminal 2)
docker compose -f docker-compose.full.yml exec producer python producer.py "Hello World!"
```

You'll see:
```
 [*] Waiting for messages. To exit press CTRL+C
 [x] Received: Hello World!
 [x] Done
```

## Management UI

Access the RabbitMQ Management Interface:
- URL: http://localhost:15672
- Username: `guest`
- Password: `guest`

View queues, messages, and connections in real-time.

## Project Structure

```
rabbitmq-tutorial/
├── app/
│   ├── producer.py        # Sends messages to queue
│   ├── consumer.py        # Receives messages from queue
│   └── test.py           # Test without RabbitMQ
├── config/
│   └── requirements.txt   # Python dependencies (pika)
├── docker/
│   ├── Dockerfile.producer # Producer container image
│   ├── Dockerfile.consumer # Consumer container image
│   └── .dockerignore
├── docker-compose.yml     # Setup with profiles (selective start)
├── docker-compose.full.yml # Setup without profiles (start all)
└── README.md
```

## Docker Commands Reference

### Using docker-compose.full.yml (All Services)

```bash
# Start everything
docker compose -f docker-compose.full.yml up -d

# View logs (all services)
docker compose -f docker-compose.full.yml logs -f

# View logs (specific service)
docker compose -f docker-compose.full.yml logs -f producer
docker compose -f docker-compose.full.yml logs -f consumer

# Check status
docker compose -f docker-compose.full.yml ps

# Stop everything
docker compose -f docker-compose.full.yml down
```

### Using docker-compose.yml (With Profiles)

```bash
# Start only RabbitMQ
docker compose up -d

# Start RabbitMQ + Producer
docker compose --profile producer up -d

# Start RabbitMQ + Consumer
docker compose --profile consumer up -d

# Start all services
docker compose --profile producer --profile consumer up -d

# View logs
docker compose logs -f

# Stop everything
docker compose down
```

## Prerequisites

- Docker Desktop installed and running
- Python 3.8+ (only if running locally, not in Docker)

## Troubleshooting

**Docker not running:**
```bash
# Start Docker Desktop first, then verify:
docker --version
```

**See what's running:**
```bash
docker compose ps
```

**View RabbitMQ container logs:**
```bash
docker logs rabbitmq
```

**Check queue status:**
- Visit http://localhost:15672
- Go to "Queues" tab
- Look for `task_queue`

## How It Works

### Producer (`app/producer.py`)
- Connects to RabbitMQ
- Creates a durable queue called `task_queue`
- Sends persistent messages
- Default message: "Hello RabbitMQ!"
- Exits after sending

### Consumer (`app/consumer.py`)
- Connects to RabbitMQ
- Listens to `task_queue`
- Processes messages (simulates work by counting dots)
- Sends acknowledgment after processing
- Runs continuously waiting for messages

### Message Flow
```
1. Producer → RabbitMQ queue
2. RabbitMQ → Consumer
3. Consumer processes → Acknowledges
4. Message removed from queue
```

## Advanced Usage

### Running Locally (Without Docker)

```bash
# Install dependencies
pip install -r config/requirements.txt

# Terminal 1 - Start consumer
python3 app/consumer.py

# Terminal 2 - Send messages
python3 app/producer.py "First message"
python3 app/producer.py "Second message..."
python3 app/producer.py "Third message....."
```

Messages with more dots take longer to process (1 second per dot).

### Testing Without RabbitMQ

```bash
python3 app/test.py
```

This simulates the message flow without requiring RabbitMQ.

## What You'll Learn

- Message queue concepts (producer/consumer pattern)
- Docker containerization and networking
- RabbitMQ basics (queues, durability, acknowledgments)
- Python messaging with pika library

## License

MIT License - feel free to use for learning and projects.
