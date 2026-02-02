using Confluent.Kafka;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

// Add service defaults & Aspire components.
builder.AddServiceDefaults();

var kafkaConfig = new ProducerConfig
{
    BootstrapServers = builder.Configuration["Kafka:BootstrapServers"] ?? "localhost:9092",
    AllowAutoCreateTopics = true,
    SecurityProtocol = SecurityProtocol.SaslSsl,
    SaslMechanism = SaslMechanism.OAuthBearer,
};

builder.Services.AddSingleton<IProducer<string, string>>(sp => 
    new ProducerBuilder<string, string>(kafkaConfig).Build());

var app = builder.Build();

app.MapDefaultEndpoints();

app.MapPost("/produce", async ([FromBody] ProduceRequest request, IProducer<string, string> producer) =>
{
    var topic = "test-topic";
    var message = new Message<string, string>
    {
        Key = request.Key ?? Guid.NewGuid().ToString(),
        Value = request.Value ?? "Default message value"
    };

    try
    {
        var deliveryResult = await producer.ProduceAsync(topic, message);
        return Results.Ok(new 
        { 
            Status = "Delivered", 
            deliveryResult.TopicPartitionOffset.Offset,
            deliveryResult.Value 
        });
    }
    catch (ProduceException<string, string> e)
    {
        return Results.Problem($"Delivery failed: {e.Error.Reason}");
    }
});

app.Run();

public record ProduceRequest(string? Key, string? Value);
