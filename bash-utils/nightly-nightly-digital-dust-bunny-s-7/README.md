# Nightly Digital Dust Bunny Sweeper

The digital wasteland can accumulate quite a bit of forgotten detritus. The `Nightly Digital Dust Bunny Sweeper` is your trusty companion for identifying those ancient, unused files lurking in your directories, consuming precious storage and mental bandwidth. Think of it as a robotic broom for your digital bunker!

## Features

*   Scans specified directories for files older than a configurable number of days.
*   Outputs a list of identified "dust bunnies" (files) along with their age and size.
*   Supports recursive scanning.
*   Optionally provides a command to move or delete the identified files (user discretion advised!).

## Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS] <directory>
```

### Options

*   `-d <days>`: Specify the age threshold in days. Files older than this will be considered dust bunnies. Default is 90 days.
*   `-r`: Enable recursive scanning of subdirectories.
*   `-l`: List only the files, without additional details.
*   `-h`: Display help message.

### Examples

Scan your home directory for files older than 180 days, recursively:
```bash
./src/dust_bunny_sweeper.sh -d 180 -r ~/my_bunker_logs
```

List only files older than 30 days in the current directory:
```bash
./src/dust_bunny_sweeper.sh -d 30 -l .
```

## Installation

Simply place the `dust_bunny_sweeper.sh` script in your desired location and make it executable:

```bash
chmod +x src/dust_bunny_sweeper.sh
```

## Contributing

Got an idea for a new broom attachment or a better dustpan? Feel free to contribute!
