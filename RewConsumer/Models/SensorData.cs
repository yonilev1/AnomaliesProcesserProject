using MongoDB.Bson.Serialization.Attributes;

namespace Consumer.Models;

public class SensorData
{
    [BsonElement("ObjectId")]
    public int Id { get; set; }
    [BsonElement("event_id")]
    public string EventId { get; set; } = string.Empty;
    [BsonElement("source_id")]
    public string SourceId { get; set; } = string.Empty;
    [BsonElement("timestamp")]
    public DateTime Timestamp { get; set; }
    [BsonElement("value")]
    public double Value { get; set; }
}