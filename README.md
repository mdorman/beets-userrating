# User rating support for Beets

The *beet userrating* plugin reads and manages a `userrating` tag on
your music files.

## Installation

Install package and scripts.

    $ pip install https://github.com/mdorman/beets-userrating/archive/master.zip

Add the plugin to beets configuration file.

```
plugins: (...) userrating
```

## Usage

    beet userrating -h
    Usage: beet ratings [options]
    Options:
     -h, --help   show this help message and exit

## FAQ

### Why not `beet rating`?

It turns out that the `mpdstats` plugin was already maintaining a
`rating` attribute.  It seemed easier to just adopt the `userrating`
nomenclature.
