using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using MongoDB.Driver;
using RewConsumer.Consumer;
using RewConsumer.Handler;

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