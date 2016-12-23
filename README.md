# Redeem Online Help

This is an errbot module that loads the gcode help directly from Redeem. Bring the Replicape 3D Printer Controller support into your errbot.

http://www.thing-printer.com/redeem/

http://errbot.io/

## Usage

`gcode`

List all loaded gcode.

`gcode m119`

```
Redeem: m119: Get current endstops state or set invert setting
```

This plugin may not load all gcode from Redeem and will not load the gcode class if it cannot be parsed.  See the debug log for explanation as to why a gcode module was not loaded.


## Configuration

Add the path to Redeem in your config.py for errbot.

`REDEEM_PATH = /path/to/redeem/redeem`

The path should be the actual redeem module (it should contain the gcode directory). From a fresh clone, it should be in `<clone path>/redeem`
