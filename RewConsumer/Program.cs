using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using MongoDB.Driver;
using RewConsumer.Consumer;
using RewConsumer.Handler;
using Serilog;

Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .WriteTo.File(
    path: "/app/logs/project_logs.log",
    outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss} - {Level:u3} - {Message:lj}{NewLine}{Exception}"
    ).CreateLogger();

IHost host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {
        var config = context.Configuration;
        var mongoCon = config["Mongo:ConnectionString"]!;

        services.AddSingleton<IMongoClient>(
            new MongoClient(mongoCon));

        services.AddScoped<DataHandler>();

        services.AddHostedService<DataConsumer>();

    }).Build();

host.Run();