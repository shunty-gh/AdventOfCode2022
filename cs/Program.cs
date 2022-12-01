
namespace Shunty.AoC;

internal partial class Program
{
    private static async Task Main(string[] args)
    {
        InitialiseLogging();
        var host = Host.CreateDefaultBuilder()
            .ConfigureAppConfiguration(LoadConfiguration)
            //.ConfigureServices()
            .UseSerilog()
            .Build()
            ;

        // Get DI based services eg:
        //var cfg = host.Services.GetRequiredService<IConfiguration>();

        var day = new Day01();
        await day.Run();
    }

    private static void InitialiseLogging()
    {
        var builder = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory());
        LoadConfiguration(builder);
        var cfg = builder.Build();

        var logconfig = new LoggerConfiguration()
            .MinimumLevel.Debug()
            .ReadFrom.Configuration(cfg)
            .Enrich.FromLogContext()
            .Enrich.WithProperty("App", "Aoc2022")
            // Filter out Microsoft and System information, if required.
            // Set level to LogEventLevel.Warning to get rid of pretty much all of them.
            .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
            .MinimumLevel.Override("System", LogEventLevel.Warning)
            .WriteTo.Console();

        Log.Logger = logconfig.CreateLogger()
            .ForContext("SourceContext", "Shunty.Aoc.Aoc2022");
    }

    private static void LoadConfiguration(IConfigurationBuilder builder)
    {
        var denv = DotEnvFilesConfigurationExtensions.FindDotenv();
        builder.AddEnvironmentVariables();
        if (!string.IsNullOrWhiteSpace(denv))
        {
            builder.AddDotEnvFile(denv, true, true);
        }
    }
}
