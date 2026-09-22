using Microsoft.Extensions.Hosting;
using MongoDB.Driver;

IHost host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {


    }).Build();