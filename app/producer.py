import pika
import sys
import os

def main():
    # Establish connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=int(os.getenv('RABBITMQ_PORT', 5672)),
            credentials=pika.PlainCredentials(
                os.getenv('RABBITMQ_USER', 'guest'),
                os.getenv('RABBITMQ_PASS', 'guest')
            )
        )
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