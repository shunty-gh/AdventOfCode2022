namespace Shunty.AoC;

public class Day06 : AocDaySolution
{
    public async Task Run()
    {
        var data = await AocUtils.GetDayText(6);
        var p1 = ScanInput(data.AsSpan(), 4);
        var p2 = ScanInput(data.AsSpan(), 14);

        Console.WriteLine("Day 6");
        Console.WriteLine($"  Part 1: {p1}");
        Console.WriteLine($"  Part 2: {p2}");
    }

    private int ScanInput(ReadOnlySpan<char> input, int packetLength)
    {
        var i = 0;
        while (i < input.Length)
        {
            var (success, idx) = ScanPacket(input.Slice(i, packetLength));
            if (success)
                return i + packetLength;
            i += idx;
        }
        throw new Exception("Unable to find an appropriate packet");
    }

    private (bool success, int dupIndex) ScanPacket(ReadOnlySpan<char> pkt)
    {
        var i = 1;
        foreach (var ch in pkt)
        {
            if (pkt.Slice(i).Contains(ch))
            {
                return (false, i);
            }
            i++;
        }
        return (true, 0);
    }
}
