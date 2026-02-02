using Confluent.Kafka;
using System.Text;

var config = new ConsumerConfig
{
    BootstrapServers = "localhost:9092",
    GroupId = "test-group",
    AutoOffsetReset = AutoOffsetReset.Earliest,
    EnableAutoCommit = false,
    SecurityProtocol = SecurityProtocol.SaslSsl,
    SaslMechanism = SaslMechanism.OAuthBearer,
};

var producerConfig = new ProducerConfig 
{ 
    BootstrapServers = "localhost:9092",
    SecurityProtocol = SecurityProtocol.SaslSsl,
    SaslMechanism = SaslMechanism.OAuthBearer,
};

using var consumer = new ConsumerBuilder<string, string>(config).Build();
using var dlqProducer = new ProducerBuilder<string, string>(producerConfig).Build();

string topic = "test-topic";
string dlqTopic = "test-topic-dlq";

consumer.Subscribe(topic);

var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) => {
    e.Cancel = true;
    cts.Cancel();
};

Console.WriteLine($"Consumer started. Listening on {topic}...");

try
{
    while (!cts.IsCancellationRequested)
    {
        try
        {
            var consumeResult = consumer.Consume(cts.Token);
            if (consumeResult == null) continue;

            Console.WriteLine($"Consumed message '{consumeResult.Message.Value}' at: '{consumeResult.TopicPartitionOffset}'.");

            try
            {
                ProcessMessage(consumeResult.Message);
                consumer.Commit(consumeResult);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error processing message: {ex.Message}. Sending to DLQ...");
                
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

                await dlqProducer.ProduceAsync(dlqTopic, dlqMessage);
                consumer.Commit(consumeResult);
            }
        }
        catch (ConsumeException e)
        {
            Console.WriteLine($"Error occurred: {e.Error.Reason}");
        }
    }
}
catch (OperationCanceledException)
{
    consumer.Close();
}

void ProcessMessage(Message<string, string> message)
{
    if (message.Value.Contains("FAIL_ME"))
    {
        throw new Exception("Simulated processing failure");
    }
}
