# nightly-void-whistle

A whimsical Node.js CLI tool that plays a unique sound when long-running tasks finish executing.

Perfect for:
- Terminal workflows
- Build processes
- Long downloads or compiles

## Installation

```sh
npm install -g nightly-void-whistle
```

## Usage

Pipe any command into `void-whistle`:

```sh
your-long-task && void-whistle
```

Or wrap it around a script:

```sh
void-whistle -- npm run build
```

## Sounds

Comes with 3 built-in sounds:
- `chime` (default)
- `bell`
- `boop`

Change the sound like this:

```sh
void-whistle --sound bell -- npm test
```

## License
MIT
