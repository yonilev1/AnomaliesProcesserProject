using MongoDB.Bson.Serialization.Attributes;
using System.Text.Json.Serialization;

namespace RewConsumer.Models;

public class SensorData
{
    [JsonPropertyName("event_id")]
    public string EventId { get; set; } = string.Empty;
    [JsonPropertyName("source_id")]
    public string SourceId { get; set; } = string.Empty;
    [JsonPropertyName("timestamp")]
    public string Timestamp { get; set; } = string.Empty;
    [JsonPropertyName("value")]
    public string Value { get; set; } = string.Empty;
}