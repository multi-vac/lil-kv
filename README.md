# lil-kv

A little append-only key-value database.

## Usage

```text
lil-kv>> set hello world
lil-kv>> get hello
world
lil-kv>>
```

## Roadmap

- [ ] Add the index.
- [ ] `set a` stores null, `get a` prints `None`.
- [ ] `get unknown` also prints `None`.
- [ ] `set -a b` doesn't work.
- [ ] `set a b c d` prints a generic error.
- [ ] `get a b` ignores `b`.
- [ ] Handle corrupted lines in the file.