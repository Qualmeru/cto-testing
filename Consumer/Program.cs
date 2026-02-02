using Confluent.Kafka;
using System.Text;

var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

builder.Services.AddHostedService<KafkaConsumerService>();

var app = builder.Build();

app.MapDefaultEndpoints();

app.Run();

public class KafkaConsumerService : BackgroundService
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<KafkaConsumerService> _logger;
    private readonly string _topic = "test-topic";
    private readonly string _dlqTopic = "test-topic-dlq";

    public KafkaConsumerService(IConfiguration configuration, ILogger<KafkaConsumerService> logger)
    {
        _configuration = configuration;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var consumerConfig = new ConsumerConfig
        {
            BootstrapServers = _configuration["Kafka:BootstrapServers"] ?? "localhost:9092",
            GroupId = "test-group",
            AutoOffsetReset = AutoOffsetReset.Earliest,
            EnableAutoCommit = false,
            SecurityProtocol = SecurityProtocol.SaslSsl,
            SaslMechanism = SaslMechanism.OAuthBearer,
        };

        var producerConfig = new ProducerConfig
        {
            BootstrapServers = _configuration["Kafka:BootstrapServers"] ?? "localhost:9092",
            SecurityProtocol = SecurityProtocol.SaslSsl,
            SaslMechanism = SaslMechanism.OAuthBearer,
        };

        using var consumer = new ConsumerBuilder<string, string>(consumerConfig).Build();
        using var dlqProducer = new ProducerBuilder<string, string>(producerConfig).Build();

        consumer.Subscribe(_topic);

        _logger.LogInformation("Consumer started. Listening on {Topic}...", _topic);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                var consumeResult = await Task.Run(() => consumer.Consume(stoppingToken), stoppingToken);
                if (consumeResult == null) continue;

                _logger.LogInformation("Consumed message '{Value}' at: '{Offset}'.", 
                    consumeResult.Message.Value, consumeResult.TopicPartitionOffset);

                try
                {
                    ProcessMessage(consumeResult.Message);
                    consumer.Commit(consumeResult);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error processing message. Sending to DLQ...");

                    var dlqMessage = new Message<string, string>
                    {
                        Key = consumeResult.Message.Key,
                        Value = consumeResult.Message.Value,
                        Headers = new Headers
                        {
                            { "exception-message", Encoding.UTF8.GetBytes(ex.Message) },
                            { "original-topic", Encoding.UTF8.GetBytes(consumeResult.Topic) }
                        }
                    };

                    await dlqProducer.ProduceAsync(_dlqTopic, dlqMessage, stoppingToken);
                    consumer.Commit(consumeResult);
                }
            }
            catch (OperationCanceledException)
            {
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred in consumer loop.");
            }
        }

        consumer.Close();
    }

    private void ProcessMessage(Message<string, string> message)
    {
        if (message.Value.Contains("FAIL_ME"))
        {
            throw new Exception("Simulated processing failure");
        }
    }
}
