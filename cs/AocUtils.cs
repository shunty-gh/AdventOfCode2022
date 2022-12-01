namespace Shunty.AoC;

public static class AocUtils
{
    public static async Task<IEnumerable<string>> GetDayLines(int day)
    {
        var fn = FindInputFile(day);
        if (string.IsNullOrEmpty(fn))
            throw new FileNotFoundException($"Input file for day {day} not found");

        return (await File.ReadAllLinesAsync(fn))
            .Select(s => s.Trim(new char[] { ' ', '\r', '\n', '\t' }))
            .ToList();
    }

    public static string FindInputFile(int day)
    {
        var dstart = Directory.GetCurrentDirectory();
        var dir = dstart;
        var dayfile = $"day{day:D2}-input";
        int maxParentLevels = 6;
        int parentLevel = 0;
        while (parentLevel <= maxParentLevels)
        {
            // Look in the directory
            var fn = Path.Combine(dir, dayfile);
            if (File.Exists(fn))
            {
                return fn;
            }

            // Look in ./input directory
            fn = Path.Combine(dir, "input", dayfile);
            if (File.Exists(fn))
            {
                return fn;
            }

            // Otherwise go up a directory
            var dinfo = Directory.GetParent(dir);
            if (dinfo == null)
            {
                break;
            }
            parentLevel++;
            dir = dinfo.FullName;
        }
        // Not found
        return "";
    }
}