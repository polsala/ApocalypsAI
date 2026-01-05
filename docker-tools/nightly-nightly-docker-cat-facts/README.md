Nightly Docker Cat Facts

A tiny Docker container that fetches a random cat fact from catfact.ninja and displays it with a cute ASCII cat.

Usage
-----

docker run --rm polsala/nightly-docker-cat-facts

The container will print something like:

  /\\_/\\  
 ( o.o ) 
  > ^ <  

\"Did you know? Cats have 32 muscles in each ear.\"

The container is built from a lightweight Go binary and is only ~5 MB.
