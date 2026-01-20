#!/bin/bash
# RabbitMQ Tutorial - Quick Start Script

echo "🐇 RabbitMQ Python Tutorial Setup"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"

# Start RabbitMQ
echo "🚀 Starting RabbitMQ..."
docker compose up -d

# Wait for RabbitMQ to be ready
echo "⏳ Waiting for RabbitMQ to start..."
sleep 10

# Check if RabbitMQ is healthy
if docker compose ps | grep -q "healthy\|running"; then
    echo "✅ RabbitMQ is ready!"
    echo ""
    echo "🌐 Management UI: http://localhost:15672"
    echo "   Username: guest"
    echo "   Password: guest"
    echo ""
#!/bin/bash
# RabbitMQ Tutorial - Quick Start Script

echo "🐇 RabbitMQ Python Tutorial Setup"
echo "=================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"

# Start RabbitMQ
echo "🚀 Starting RabbitMQ..."
docker compose up -d

# Wait for RabbitMQ to be ready
echo "⏳ Waiting for RabbitMQ to start..."
sleep 10

# Check if RabbitMQ is healthy
if docker compose ps | grep -q "healthy\|running"; then
    echo "✅ RabbitMQ is ready!"
    echo ""
    echo "🌐 Management UI: http://localhost:15672"
    echo "   Username: guest"
    echo "   Password: guest"
    echo ""
    echo "📝 Testing options:"
    echo ""
    echo "  Option 1 - Local Python (requires virtual env):"
    echo "   Terminal 1: python3 app/consumer.py"
    echo "   Terminal 2: python3 app/producer.py 'Hello World!'"
    echo ""
    echo "  Option 2 - Docker containers:"
    echo "   docker compose --profile producer up -d"
    echo "   docker compose --profile consumer up -d"
    echo ""
    echo "  Option 3 - Run test (no RabbitMQ needed):"
    echo "   python3 app/test.py"
    echo ""
    echo "🛑 To stop: docker compose down"
else
    echo "❌ RabbitMQ failed to start properly"
    echo "Check logs: docker compose logs"
    exit 1
fi