# Nightly Scavenger's Manifest Generator

## Description
In the post-apocalyptic digital wasteland, data hoards can be vast and chaotic. The Nightly Scavenger's Manifest Generator is a crucial utility for any diligent scavenger, providing a quick, high-level overview of the files within a specified directory. It scans through the directory and its subdirectories, compiling a manifest that details total file counts, total size, unique file extensions found, and a breakdown of counts, sizes, and the latest modification time for each file type.

This tool helps you quickly assess the contents of a data cache without needing to delve into every individual file, making it easier to prioritize your digital salvage operations.

## Usage
To generate a manifest, simply run the `manifest_generator.py` script with the target directory path as an argument.

```bash
python src/manifest_generator.py /path/to/your/data_hoard
```

### Example Output
The utility outputs a JSON object to standard output. Here's an example:

```json
{
  "directory": "/path/to/your/data_hoard",
  "summary": {
    "total_files": 5,
    "total_directories": 2,
    "total_size_bytes": 12345,
    "unique_extensions": [".json", ".log", ".txt", "no_extension"]
  },
  "file_type_breakdown": {
    ".txt": {
      "count": 2,
      "total_size_bytes": 1000,
      "latest_modified": "2023-01-05T00:00:00Z"
    },
    ".json": {
      "count": 1,
      "total_size_bytes": 2345,
      "latest_modified": "2023-01-03T14:00:00Z"
    },
    ".log": {
      "count": 1,
      "total_size_bytes": 500,
      "latest_modified": "2023-01-04T15:00:00Z"
    },
    "no_extension": {
      "count": 1,
      "total_size_bytes": 800,
      "latest_modified": "2023-01-02T10:00:00Z"
    }
  }
}
```
