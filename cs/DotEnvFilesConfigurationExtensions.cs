namespace Shunty.AoC;

public static class DotEnvFilesConfigurationExtensions
{
	public static IConfigurationBuilder AddDotEnvFile(this IConfigurationBuilder builder, string path, bool optional, bool reloadOnChange)
	{
		if (builder is null)
		{
			throw new ArgumentNullException("builder");
		}
		if (string.IsNullOrEmpty(path))
		{
			throw new ArgumentException("Path must be a non-empty, valid file path");
		}
		var fn = Path.GetFileName(path);
		if (fn != ".env")
		{
			throw new ArgumentException("File must be a .env file");
		}
		if (!File.Exists(path) && !optional)
		{
			throw new ArgumentException("Path must be a valid file path");
		}

		var dir = Path.GetDirectoryName(path) ?? "";
		return builder.AddIniFile(s =>
		{
			s.FileProvider = new PhysicalFileProvider(dir, ExclusionFilters.None);
			s.Path = fn;
			s.Optional = optional;
			s.ReloadOnChange = reloadOnChange;
		});
	}

    public static string FindDotenv()
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