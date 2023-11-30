
static class Program
{
    private static IConfiguration? _config;
    public static IConfiguration Configuration
    {
        get
        {
            if (_config == null)
            {
                var (pub, priv) = FindSettingsFiles();
                var denv = FindDotenv();
                var cb = new ConfigurationBuilder();

                if (!string.IsNullOrWhiteSpace(pub))
                {
                    cb.AddJsonFile(pub, optional: false, reloadOnChange: true);
                }
                if (!string.IsNullOrWhiteSpace(priv))
                {
                    cb.AddJsonFile(priv, optional: true);
                }
                cb.AddEnvironmentVariables();
                if (!string.IsNullOrWhiteSpace(denv))
                {
                    cb.AddDotEnvFile(denv, true, true);
                }
                _config = cb.Build();
            }
            return _config;
        }
    }

    static async Task Main(string[] args)
    {
        // NB: In C# the args array DOES NOT contain the program name as the first element
        // However, if you use the Environment.GetCommandLineArgs() it DOES include the program name

        try
        {
            var year = DateTime.Today.Year;
            if (args.Length == 0)
            {
                // Show usage
                Console.WriteLine();
                Console.WriteLine("  *** Advent Of Code *** ");
                Console.WriteLine(" --- Fetch input data --- ");
                Console.WriteLine();
                Console.WriteLine(" Usage: ");
                Console.WriteLine("   $> fetch-aoc-data <day-no> [year=<year-no>]");
                Console.WriteLine();
                Console.WriteLine(" Where <day-no> is an appropriate day number from 1..25 and the optional year parameter");
                Console.WriteLine($" allows you to set the specific year required. Defaults to the current year ({year}).");
                Console.WriteLine();
                Console.WriteLine(" You must have an appsettings.private.json file with a valid/authenticated 'sessionCookie'");
                Console.WriteLine(" setting for this program to download input for the Advent Of Code site.");
                Console.WriteLine();
                return;
            }

            // Get the first argument - which should be an int from 1..25
            if (!int.TryParse(args[0], out var dn) || dn < 1 || dn > 25)
            {
                throw new ArgumentException("Please specify a valid day number from 1..25");
            }

            // Look for a year arg, maybe
            if (args.Length > 1)
            {
                if (args.Any(a => a.ToLower().StartsWith("year=")))
                {
                    var ytxt = args.First(a => a.ToLower().StartsWith("year=")).Substring(5);
                    if (int.TryParse(ytxt, out var cli_year))
                    {
                        year = cli_year;
                    }
                }
            }
            var fn = await FindInput(dn, year);
            Console.WriteLine();
            Console.WriteLine($"Input file for day {dn}/{year} successfully retrieved");
            Console.WriteLine();
        }
        catch (Exception ex)
        {
            Console.WriteLine();
            Console.WriteLine(" *** Advent Of Code Error *** ");
            Console.WriteLine(" Failed to fetch input data.");
            Console.WriteLine($" {ex.Message}");
            Console.WriteLine();
        }
    }

    static string DayFileName(int day) => $"day{day:D2}-input";

    /// <summary>
    /// Find the file containing the text input for the given day. Try and download it
    /// from AoC if it can't be found on disk.
    /// </summary>
    /// <param name="day">The day number</param>
    /// <returns>A string containing the path name of the file, if found</returns>
    public static async Task<string> FindInput(int day, int year)
    {
        var inputDir = FindInputDirectory();
        var fn = Path.Combine(inputDir, DayFileName(day));

        if (File.Exists(fn))
            return fn;

        // Try and download it
        await DownloadInput(day, inputDir, year);
        return fn;
    }


    static readonly Uri baseAddress = new Uri("https://adventofcode.com/");
    private static async Task DownloadInput(int day, string outputDir, int year = 0)
    {
        if (year == 0)
            year = DateTime.Today.Year;

        // Need to have the session cookie available
        var cookie = Program.Configuration["sessionCookie"];
        if (string.IsNullOrWhiteSpace(cookie))
        {
            throw new KeyNotFoundException("Session cookie not set. Cannot download daily input. Please add a 'sessionCookie' setting to appsettings.json or (better) to appsettings.private.json");
        }
        // Check the day
        var requiredDate = new DateTime(year, 12, day);
        if (DateTime.Today < requiredDate)
        {
            throw new ArgumentException($"Input file for day {day}/{year} will not be available yet. Have patience!");
        }

        var fragment = $"{year}/day/{day}/input";
        var cookies = new CookieContainer();
        var fn = Path.Combine(outputDir, DayFileName(day));
        using (var handler = new HttpClientHandler { CookieContainer = cookies })
        using (var client = new HttpClient(handler) { BaseAddress = baseAddress })
        {
            cookies.Add(baseAddress, new Cookie("session", cookie));
            var response = await client.GetAsync(fragment);
            if (!response.IsSuccessStatusCode)
            {
                if (response.StatusCode == HttpStatusCode.NotFound)
                {
                    throw new FileNotFoundException($"Input file for day {day}/{year} not found");
                }
                else
                {
                    throw new ApplicationException($"Error trying to download the input file for day {day}/{year};{Environment.NewLine}This may indicate that the session cookie is invalid;{Environment.NewLine}Error: {response.StatusCode}: {response.ReasonPhrase}");
                }
            }
            var content = await response.Content.ReadAsStringAsync();
            await File.WriteAllTextAsync(fn, content);
        }
    }

    private static (string publicSettings, string privateSettings) FindSettingsFiles(int maxParentLevels = 6)
    {
        var dstart = Directory.GetCurrentDirectory();
        var dir = dstart;
        var publicSettingsName = "appsettings.json";
        var privateSettingsName = "appsettings.private.json";
        string pub = "", prv = "";
        int parentLevel = 0;
        while (parentLevel <= maxParentLevels)
        {
            var fn = Path.Combine(dir, publicSettingsName);
            var fnprv = Path.Combine(dir, privateSettingsName);
            if (string.IsNullOrWhiteSpace(pub) && File.Exists(fn))
            {
                pub = fn;
            }
            if (string.IsNullOrWhiteSpace(prv) && File.Exists(fnprv))
            {
                prv = fnprv;
            }

            if (!string.IsNullOrWhiteSpace(pub) && !string.IsNullOrWhiteSpace(prv))
            {
                break;
            }

            var dinfo = Directory.GetParent(dir);
            if (dinfo == null)
            {
                break;
            }
            parentLevel++;
            dir = dinfo.FullName;
        }
        return (pub, prv);
    }

    private static string FindInputDirectory()
    {
        var dstart = Directory.GetCurrentDirectory();
        var dir = dstart;
        var inputDirName = "input";
        int maxParentLevels = 6;
        int parentLevel = 0;
        while (parentLevel <= maxParentLevels)
        {
            var dn = Path.Combine(dir, inputDirName);
            if (Directory.Exists(dn))
            {
                return dn;
            }

            var dinfo = Directory.GetParent(dir);
            if (dinfo == null)
            {
                break;
            }
            parentLevel++;
            dir = dinfo.FullName;
        }
        throw new DirectoryNotFoundException("Cannot find the directory for the input data. Please create an 'input' directory within the project structure.");
    }

    private static string FindDotenv()
    {
        var dstart = Directory.GetCurrentDirectory();
        var dir = dstart;
        var envfile = ".env";
        int maxParentLevels = 6;
        int parentLevel = 0;
        while (parentLevel <= maxParentLevels)
        {
            var denv = Path.Combine(dir, envfile);
            if (File.Exists(denv))
            {
                return denv;
            }

            var dinfo = Directory.GetParent(dir);
            if (dinfo == null)
            {
                break;
            }
            parentLevel++;
            dir = dinfo.FullName;
        }
        // No .env found
        return "";
    }

}