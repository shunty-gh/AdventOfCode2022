# Advent Of Code
## Fetch daily input data

This tiny application is a C# program to get the daily input data for the [Advent Of Code](https://adventofcode.com) puzzles.

It can be built and run under Windows or Linux.

In order to be a good AoC citizen it will only download input data that we haven't already downloaded. Data is located in, and downloaded to, the `<project_root>/input` directory and each day file has a name of the form `day01-input`.

You will need have logged in to the site previously to get data specific to you. See the [Session Cookie](#session-cookie) section below.

### Build

#### Linux

```sh
$> cd <project_root_dir>/fetch
$> ./build-release.sh
```

#### Windows

```powershell
$> cd <project_root_dir>\fetch
$> .\build-release
```

This will build a (fairly large) single file program executable and then copy it to the project root directory. From there it can be run from the command line as normal.

### Run

After building the program using the supplied script/batch file:

#### Linux

```sh
$> cd <project_root_dir>
$> ./fetch-aoc-data <day_no> [year=<year_no>]
```

#### Windows

```powershell
$> cd <project_root_dir>
$> .\fetch-aoc-data <day_no> [year=<year_no>]
```

Alternatively it can be run from within the `fetch` directory using the `dotnet` command line (in Windows or Linux):

```
$> dotnet run <day_no> [year=<year_no>]
```

Running the program without any parameters will print out usage instructions. The <day_no> is required and should be in the range 1..25 to indicate which days data is wanted. An optional `year=`` parameter can be supplied if you want to work with previous year data.

### Session Cookie

The program requires an authenticated session cookie in order to access the AoC site and download the correct data. The easiest way to get this is to go to the [AoC](https://adventofcode.com) site in a web browser and login, then open up the developer tools on the web browser (usually F12 or Ctrl+Shift+I). Then goto the `Application` tab in the tools and find the `session` cookie under the `Storage -> Cookies` section. Alternatively look in the network tab for a request to the site, click on the request, then on the Headers tab and look for the session cookie among the request headers.

Once you have copied the cookie you need to paste it into a settings file named `appsettings.private.json` or into a `.env` file in the project or workspace root. **Do not check this file into your source code repository**. For example:

```
{
    "sessionCookie": "12345c7465897f5f42456c5d01f64e0ec3d0b9f9b81cd42c977cc8a27fb54e6495d76bc649147157bcc8cd5cffba1523df321f3eb4ae3bfb89c10d15d608fff2"
}
```
for an `appsettings.json` file

or

```
sessionCookie=12345c7465897f5f42456c5d01f64e0ec3d0b9f9b81cd42c977cc8a27fb54e6495d76bc649147157bcc8cd5cffba1523df321f3eb4ae3bfb89c10d15d608fff2
```
(all on a single line) for a `.env` file.

If the session cookie does not exist, or is incorrect or outdated/expired the application will not work and you will need to login again and get a new cookie.