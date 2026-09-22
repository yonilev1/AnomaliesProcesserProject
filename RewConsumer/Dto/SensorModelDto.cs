using MongoDB.Bson.Serialization.Attributes;

namespace RewConsumer.Dto;

public class SensorDataDto
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