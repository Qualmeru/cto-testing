# Kafka Microservices Demo (.NET 10 & Aspire)

This project demonstrates a Kafka producer and consumer using ASP.NET Core APIs and .NET Aspire orchestration, fully targeting .NET 10.

## Features

- **.NET 10**: All projects target .NET 10.0.
- **.NET Aspire**: Orchestrates the Producer and Consumer microservices.
- **OpenTelemetry**: Integrated via .NET Aspire Service Defaults for tracing, metrics, and logging.
- **Producer API**: A Web API with a `POST /produce` endpoint to send messages to Kafka.
- **Consumer API**: A Web API with a background service that consumes messages and handles errors.
- **Dead Letter Queue (DLQ)**: Failed messages are automatically sent to a DLQ topic with error headers.
- **Security**: Configured for `SaslSsl` and `OAuthBearer` for secure Kafka communication.
- **Efficient Formatting**: Uses Minimal APIs and modern C# patterns.

## Structure

- **KafkaDemo.AppHost**: The Aspire orchestrator.
- **KafkaDemo.ServiceDefaults**: Common configurations for OpenTelemetry, health checks, and service discovery.
- **Producer**: Web API that produces messages.
- **Consumer**: Web API that consumes messages and handles DLQ.

## How to Run

1.  **Start Kafka**:
    ```bash
    docker-compose up -d
    ```
    *Note: The included docker-compose is configured for PLAINTEXT. To use SaslSsl/OAuthBearer as configured in the code, a properly secured Kafka cluster is required.*

2.  **Run the Solution via Aspire**:
    ```bash
    cd KafkaDemo.AppHost
    dotnet run
    ```

3.  **Produce a Message**:
    Find the Producer URL on the Aspire Dashboard, then:
    ```bash
    curl -X POST http://<producer-url>/produce \
         -H "Content-Type: application/json" \
         -d '{"key": "test-key", "value": "Hello Kafka!"}'
    ```

4.  **Test DLQ**:
    Send a message containing `FAIL_ME` to trigger the DLQ logic:
    ```bash
    curl -X POST http://<producer-url>/produce \
         -H "Content-Type: application/json" \
         -d '{"value": "This message will FAIL_ME"}'
    ```
