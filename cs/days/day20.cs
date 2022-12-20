namespace Shunty.AoC;

public class Day20 : AocDaySolution
{
    public async Task Run()
    {
        var data = (await AocUtils.GetDayLines(20)).ToList();

        Console.WriteLine("Day 20");
        Console.WriteLine($"  Part 1: {MixList(data, 1, 1)}");
        Console.WriteLine($"  Part 2: {MixList(data, 811589153, 10)}");
    }

    public Int64 MixList(List<string> input, Int64 mult, int count)
    {
        var nums = input
            .Select((ln, idx) => new { Index = idx, Value = Int64.Parse(ln) * mult })
            .ToList();

        var nc = nums.Count;
        foreach (var _ in Enumerable.Range(0, count))
        {
            foreach (var i in Enumerable.Range(0, nc))
            {
                var ix = nums.FindIndex(n => n.Index == i);
                var el = nums[ix];
                nums.RemoveAt(ix);
                nums.Insert((int)GetModIndex(ix + el.Value, nc - 1), el);
            }
        }
        var zeroindex = nums.FindIndex(n => n.Value == 0);
        return nums[(zeroindex + 1000) % nc].Value
            + nums[(zeroindex + 2000) % nc].Value
            + nums[(zeroindex + 3000) % nc].Value;
    }

    public Int64 GetModIndex(Int64 index, int mod)
    {
        if (index < 0)
            return ((index % mod) + mod) % mod;
        return index % mod;
    }
}
