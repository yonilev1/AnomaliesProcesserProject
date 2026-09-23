using Confluent.Kafka;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using RewConsumer.Handler;
using System.Text.Json;
using RewConsumer.Models;
namespace RewConsumer.Consumer;

public class DataConsumer : BackgroundService
{
    private readonly ILogger<DataConsumer> _logger;
    private readonly IServiceScopeFactory _factory;
    private readonly string _bootstrapServer;
    private readonly IConsumer<Null, string> _consumer;
    private readonly string _topic;

    public DataConsumer(
        ILogger<DataConsumer> logger,
        IServiceScopeFactory factory,
        IConfiguration configuration
        )
    {
        _logger = logger;
        _factory = factory;
        _bootstrapServer = configuration["Kafka:BootstrapServer"] ?? "localhost:9092";
        _topic = configuration["Kafka:Topic"] ?? "activity-readings";

        ConsumerConfig config = new ConsumerConfig
        {
            BootstrapServers = _bootstrapServer,
            GroupId = "activity-group",
            AutoOffsetReset = AutoOffsetReset.Earliest
        };

        _consumer = new ConsumerBuilder<Null, string>(config).Build();
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _consumer.Subscribe(_topic);

        _logger.LogInformation($"Started consuming from topic: {_topic}");

        try
        {
            while(!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    var consumed = _consumer.Consume(stoppingToken);

                    if (consumed == null || consumed.Message.Value == null)
                        continue;

                    var deserilizedData = JsonSerializer.Deserialize<SensorData>(consumed.Message.Value);
                    using (var scope = _factory.CreateScope())
                    {
                        var handler = scope.ServiceProvider.GetRequiredService<DataHandler>();
                        await handler.HandleAsync(deserilizedData);
                    }
                    _logger.LogInformation($"Successfully procssed rew data from {deserilizedData.SourceId} to Mongo");
                }
                catch (ConsumeException ex)
                {
                    _logger.LogError($"Kafka consume error: {ex.Error.Reason}");
                }
                catch (JsonException ex)
                {
                    _logger.LogError($"JSON Deserialization error: {ex.Message}");
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error processing message in handler");
                }
            }
        }
        catch (OperationCanceledException)
        {
            _logger.LogInformation("Consumption canceled by the host.");
        }
        finally
        {
            _consumer.Close();
        }

    }
}