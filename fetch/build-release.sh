#!/bin/bash
echo Building standalone executable for linux-x64...
dotnet publish -c Release -r linux-x64

echo Copying to project root...
cp ./bin/Release/net8.0/linux-x64/publish/fetch-aoc-data ..
