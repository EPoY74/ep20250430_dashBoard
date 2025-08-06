// string
string s = "";
var sw1 = Stopwatch.StartNew();
for (int i = 0; i < 10000; i++)
{
    s += "x";
}
sw1.Stop();
Console.WriteLine($"string: {sw1.ElapsedMilliseconds} ms");

// StringBuilder
var sb = new StringBuilder();
var sw2 = Stopwatch.StartNew();
for (int i = 0; i < 10000; i++)
{
    sb.Append("x");
}
sw2.Stop();
Console.WriteLine($"StringBuilder: {sw2.ElapsedMilliseconds} ms");
