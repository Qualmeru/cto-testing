using Aspire.Hosting;
using System.Runtime.CompilerServices;

var builder = DistributedApplication.CreateBuilder(args);

// Get the directory where this file is located (at compile time)
string projectDir = GetSourceDirPath();

builder.AddProject("producer", Path.Combine(projectDir, "../Producer/Producer.csproj"));
builder.AddProject("consumer", Path.Combine(projectDir, "../Consumer/Consumer.csproj"));

builder.Build().Run();

static string GetSourceDirPath([CallerFilePath] string? filePath = null) 
    => Path.GetDirectoryName(filePath)!;
