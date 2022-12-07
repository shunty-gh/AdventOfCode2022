namespace Shunty.AoC;

public class Day07 : AocDaySolution
{
    internal readonly record struct AoCFile(string Name, Int64 Size);

    internal class AoCDirectory
    {
        public string Name { get; init; }
        public AoCDirectory? Parent { get; init; }
        private List<AoCDirectory> _dirs = new();
        private List<AoCFile> _files = new();
        public IEnumerable<AoCDirectory> Directories => _dirs;
        public IEnumerable<AoCFile> Files => _files;

        public AoCDirectory(string name, AoCDirectory? parent)
        {
            Name = name;
            Parent = parent;
            Parent?._dirs.Add(this);
        }

        public AoCDirectory AddDirectory(string name) => new AoCDirectory(name, this);

        public void AddFile(string name, Int64 size) => _files.Add(new AoCFile(name, size));

        public AoCDirectory FindDirectory(string name)
        {
            return name == ".."
                ? this.Parent ?? this
                : _dirs.FirstOrDefault(d => d.Name == name) ?? this;
        }
    }

    private Int64 GetDirectorySizes(AoCDirectory dir, Dictionary<string, Int64> sizes, string path = "")
    {
        var fullpath = dir.Name == "/" ? "/" : $"{path}{dir.Name}/";
        var sz = dir.Files.Sum(f => f.Size);
        foreach (var d in dir.Directories)
        {
            sz += GetDirectorySizes(d, sizes, fullpath);
        }
        sizes[fullpath] = sz;
        return sz;
    }

    private const Int64 TotalDiskSpace = 70000000L;
    private const Int64 RequiredDiskSpace = 30000000L;

    public async Task Run()
    {
        var data = await AocUtils.GetDayLines(7);
        var root = BuildFileSystem(data);

        var dirsizes = new Dictionary<string, Int64>();
        GetDirectorySizes(root, dirsizes);
        var freespace = TotalDiskSpace - dirsizes["/"];
        var needed = RequiredDiskSpace - freespace;

        Console.WriteLine("Day 7");
        Console.WriteLine($"  Part 1: {dirsizes.Values.Where(v => v <= 100000).Sum()}");
        Console.WriteLine($"  Part 2: {dirsizes.Values.Where(v => v >= needed).Min()}");
    }

    private AoCDirectory BuildFileSystem(IEnumerable<string> input)
    {
        var root = new AoCDirectory("/", null);
        var cwd = root;
        foreach (var line in input.Skip(2))
        {
            var splits = line.Split(' ');
            switch (splits[0])
            {
                case "$":
                    if (splits[1] == "cd")
                    {
                        cwd = cwd.FindDirectory(splits[2]);
                    }
                    break;
                case "dir":
                    cwd.AddDirectory(splits[1]);
                    break;
                default:
                    cwd.AddFile(splits[1], Int64.Parse(splits[0]));
                    break;
            }
        }
        return root;
    }
}
