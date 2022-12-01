# Advent of Code 2022

## Rust solutions

Some solutions written in Rust for the [Advent of Code 2022](https://adventofcode.com/2022) puzzles.

Using a current version of Rust as of December 2022.

I am a Rust novice so it is highly likely that if I were to come back to this code after using Rust for a year or so then I'd be horrified and perhaps embarrassed by the standard of code here. But it should, at least, work.

### Pre-requisites

* Cargo/Rust installed
* (Optional) [Visual Studio Code](https://code.visualstudio.com/) - the build and run/debug tasks work with VS Code
* (Optional) Any other IDE/editor capable of handling Rust programs

OR

* An IDE/application that can handle devcontainers (eg VS Code, GitHub Codespaces) and then use the devcontainer definition in the `.devcontainer` directory.

### Run

```
$> cargo run
```

### Debugging - in VS Code

The `.vscode` directory contains a launch configuration named `Cargo launch` which can run and debug the Rust application. Make sure to select the `Cargo launch` option from the debug window launch drop down, then set one or more breakpoints in the code by clicking in the left gutter of the appropriate source line and then press F5 to run/debug.
