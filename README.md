# Kafka Microservices Demo (.NET 10)

This project demonstrates a simple Kafka producer and consumer using C# and .NET. 
Note: Although the projects are configured for .NET 8.0 to ensure compatibility with the current environment, they are designed to be easily upgraded to .NET 10.

## Structure

- **Producer**: A console application that sends messages to a Kafka topic.
- **Consumer**: A console application that consumes messages and handles errors using a Dead Letter Queue (DLQ).
- **docker-compose.yml**: Sets up Kafka and Zookeeper.

## How to Run

1.  **Start Kafka**:
    ```bash
    docker-compose up -d
    ```

2.  **Run the Consumer**:
    ```bash
    cd Consumer
    dotnet run
    ```

3.  **Run the Producer**:
    ```bash
    cd Producer
    dotnet run
    ```

## Features

- **Dead Letter Queue (DLQ)**: If the consumer fails to process a message (simulated by sending a message containing "FAIL_ME"), it redirects the message to `test-topic-dlq` with added headers containing the error message.
- **Top-level statements**: Efficient and clean code formatting.
- **Manual Commits**: Ensures messages are only marked as processed after successful handling or being sent to the DLQ.
