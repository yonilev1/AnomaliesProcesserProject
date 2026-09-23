using DnsClient.Internal;
using Microsoft.Extensions.Logging;
using MongoDB.Driver;
using RewConsumer.Dto;
using RewConsumer.Models;
namespace RewConsumer.Handler;


public class DataHandler
{
    private readonly IMongoClient _client;
    private readonly IMongoDatabase _database;
    private readonly IMongoCollection<SensorDataDto> _collection;
    private readonly ILogger<DataHandler> _logger;

    public DataHandler(IMongoClient client, ILogger<DataHandler> logger)
    {
        _client = client;
        _database = _client.GetDatabase("sensor_data");
        //_database.CreateCollection("raw_readings");
        _collection = _database.GetCollection<SensorDataDto>("raw_readings");
        _logger = logger;
    }

    public async Task HandleAsync(SensorData data)
    {
        if(ValidateData(data))
        {
            SensorDataDto fullSensor = new SensorDataDto
            {
                EventId = data.EventId,
                SourceId = data.SourceId,
                Timestamp = DateTime.Parse(data.Timestamp),
                Value = double.Parse(data.Value)
            };
            await _collection.InsertOneAsync(fullSensor);
        }
    }

    public bool ValidateData(SensorData data)
    {
        if (string.IsNullOrEmpty(data.EventId))
        {
            _logger.LogWarning($"Error: data from {data.SourceId} is missing Event Id.");
            return false;
        }
        if (string.IsNullOrEmpty(data.SourceId))
        {
            _logger.LogWarning($"Error: data number {data.EventId} is missing Source Id.");
            return false;
        }
        if (!DateTime.TryParse(data.Timestamp, out var _))
        {
            _logger.LogWarning($"Error: data number {data.EventId} has a bad value for the date.");
            return false;
        }
        if (!double.TryParse(data.Value, out var _))
        {
            _logger.LogWarning($"Error: data number {data.EventId} has bad value.");
            return false;
        }
        return true;
    }
}