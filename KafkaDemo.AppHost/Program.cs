using Aspire.Hosting;

var builder = DistributedApplication.CreateBuilder(args);

builder.AddProject("producer", "../Producer/Producer.csproj");
builder.AddProject("consumer", "../Consumer/Consumer.csproj");

builder.Build().Run();
