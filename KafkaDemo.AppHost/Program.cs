using Aspire.Hosting;
using System.Runtime.CompilerServices;

namespace KafkaDemo.AppHost;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = DistributedApplication.CreateBuilder(args);

        // Absolute path resolution to avoid "Project not found" errors
        string appHostDir = GetSourceDirPath();
        string producerPath = Path.GetFullPath(Path.Combine(appHostDir, "../Producer/Producer.csproj"));
        string consumerPath = Path.GetFullPath(Path.Combine(appHostDir, "../Consumer/Consumer.csproj"));

        builder.AddProject("producer", producerPath);
        builder.AddProject("consumer", consumerPath);

        builder.Build().Run();
    }

    private static string GetSourceDirPath([CallerFilePath] string? filePath = null) 
        => Path.GetDirectoryName(filePath)!;
}
