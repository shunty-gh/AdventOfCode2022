namespace Shunty.AoC;

public class Day01
{
    public async Task Run()
    {
        var lines = await AocUtils.GetDayLines(1);
        var calories = new List<int> { 0 };
        foreach(var cal in lines)
        {
            if (string.IsNullOrEmpty(cal))
            {
                calories.Add(0);
                continue;
            }
            calories[calories.Count - 1] += int.Parse(cal);
        };

        calories.Sort();
        Console.WriteLine("Day 1");
        Console.WriteLine($"  Part 1: {calories.Last()}");
        Console.WriteLine($"  Part 2: {calories.TakeLast(3).Sum()}");
    }
}
