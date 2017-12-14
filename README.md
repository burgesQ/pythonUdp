# pythonUdp

A simple tool that allow you to test the output of a UDP / SSL server.

# Usage

```
~/repo/pythonUdp master*
19:48:46 ❯ ./pythonUdp -h                                                             [0]
Usage : ./test [-i ip][-p port][-o output_file][-a sizeChunk][-k key.pem -c cert.pem][-h]

          -i --ip      : Ip address to connect.
          -p --port    : Port to connect.
          -o --output  : Output file from the server.
          -a --async   : Asynchronus test. Must be > 0
          -k --key     : SSL key
          -c --cert    : SSL certificat
```


# Default values

| Parameter               | Value          |
|-------------------------|----------------|
| ip                      | localhost      |
| port                    | 4242           |
| output file             | none (disable) |
| async / size of a chunk | 0 (disable)    |
| ssl key                 | none (disable) |
| ssl cert                | none (disable) |

# Tests

The tests have to be written in the pythonUdp file (what a sham I know)

The process is quiet simple, edit the tests global variable (line 12) :

```
tests = [
    # [ Title of the test, expected output, content send ]
    [ "Test one. Simple string. Expected : ", "PONG", "PING" ],
]

```


[TODO.md](TODO)
