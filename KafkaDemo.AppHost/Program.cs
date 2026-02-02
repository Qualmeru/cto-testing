using Aspire.Hosting;

namespace KafkaDemo.AppHost;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = DistributedApplication.CreateBuilder(args);

        builder.AddProject<Projects.Producer>("producer");
        builder.AddProject<Projects.Consumer>("consumer");

        builder.Build().Run();
    }
}
