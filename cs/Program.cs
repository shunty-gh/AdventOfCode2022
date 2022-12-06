namespace Shunty.AoC;

public interface AocDaySolution
{
    Task Run();
}

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

        Console.WriteLine();
        Console.WriteLine("*** Advent Of Code 2022 (C#) ***");
        Console.WriteLine();
        foreach (var t in new Type[] { typeof(Day01), typeof(Day06) })
        {
            var day = Activator.CreateInstance(t) as AocDaySolution;
            if (day != null)
            {
                await day.Run();
                Console.WriteLine();
            }
        }
        Console.WriteLine();
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
