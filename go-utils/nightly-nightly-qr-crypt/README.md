# nightly-qr-crypt

**Nightly QR Crypt** – a tiny, whimsical command‑line tool that turns any string into an 8×8 ASCII QR‑like pattern. It hashes the input with SHA‑256 and maps the first 64 bits to a grid of "#" (black) and space (white). Perfect for secret notes in the wasteland.

## Usage

```bash
# Run without building (requires Go installed)
go run src/main.go "Hello World"
```

Or build it first:

```bash
go build -o qrcrypt src/main.go
./qrcrypt "Your secret message"
```

If you forget to pass a string, the tool prints a short usage message.

## Example

```bash
$ ./qrcrypt "test"
#  #####
#    ## 
## #    
#      #
#   #   
 #  ##  
 ##### #
 ##  # #
```

The output is deterministic – the same input always yields the same pattern.

## License

MIT © ApocalypsAI
