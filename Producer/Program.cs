using Confluent.Kafka;

var config = new ProducerConfig
{
    BootstrapServers = "localhost:9092",
    AllowAutoCreateTopics = true
};

using var producer = new ProducerBuilder<string, string>(config).Build();
string topic = "test-topic";

Console.WriteLine($"Producer started. Sending messages to {topic}...");

for (int i = 0; i < 10; i++)
{
    var message = new Message<string, string>
    {
        Key = Guid.NewGuid().ToString(),
        Value = $"Message {i}: {DateTime.Now}"
    };

    try
    {
        var deliveryResult = await producer.ProduceAsync(topic, message);
        Console.WriteLine($"Delivered '{deliveryResult.Value}' to '{deliveryResult.TopicPartitionOffset}'");
    }
    catch (ProduceException<string, string> e)
    {
        Console.WriteLine($"Delivery failed: {e.Error.Reason}");
    }

    await Task.Delay(1000);
}

// Send a "bad" message to demonstrate DLQ
var badMessage = new Message<string, string>
{
    Key = "bad-key",
    Value = "FAIL_ME"
};

await producer.ProduceAsync(topic, badMessage);
Console.WriteLine("Sent message that should fail in consumer.");

producer.Flush(TimeSpan.FromSeconds(10));
