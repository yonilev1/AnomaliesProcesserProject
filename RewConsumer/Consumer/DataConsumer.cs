using Confluent.Kafka;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;

namespace RewConsumer.Consumer;

public class DataConsumer : BackgroundService
{
    private readonly ILogger<DataConsumer> _logger;
    private readonly IServiceScopeFactory _factory;
    private readonly string _bootstrapServer;
    private readonly IConsumer<Null, string> _consumer;
    private record string _topic;

    public DataConsumer(
        ILogger<DataConsumer> logger,
        IServiceScopeFactory factory,
        IConfiguration configuration
        )
    {
        _logger = logger;
        _factory = factory;
        _bootstrapServer = configuration["Kafka:BootstrapServers"] ?? "localhost:9092";
        _topic = configuration["Kafka:Topics:StationsInformationTopic"] ?? "bike.station-information";
    }
}