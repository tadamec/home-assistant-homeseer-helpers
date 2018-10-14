#HS-WS200+/HS-WD200+ Switch Helpers

The `hs200_led_control.py` file implements functionality change the LED display mode from
dimmer to status indicator, change the color of the individual status LEDs, set the blink
modes for the LEDs, and modify the blink frequency.

##Requirements

The script requires [Python scripting](https://www.home-assistant.io/components/python_script/)
to be enabled in your Home Assistant
`configuration.yaml` file:

```
.
.
.

# Enable python scription
python_script:

.
.
.

```

##Installation

To install the scripts, copy the [hs200_led_control.py](hs200_led_control.py) file into the
`python_scripts` directory under you Home Assistant configuration root; create the directory if
it does not already exist. Once copied, restart Home Assistant and the script should show up in
the 'Services' section as `python_script.hs200_led_control`. 

> TODO: Get somebody with a Hass.io instance to write documentation.

##Operation

Operation is performed on groups of switches using standard Home Assistant service calls.
Larger numbers of switches and operations might appear on the switches slowly. Groups must be
comprised of the Z Wave nodes in order for the script to find the appropriate attributes.

## Call Format

The script requires the group entity and one or more parameters be passed. For example, the
JSON parameter string below will change the blink frequency on the group named _example_:

```json
{
  "target_group": "group.example",
  "blink_frequency": 5
}
```

The script interrogates the `attributes` collection of the group entities for product names
specific to the supported switches, _HS-WD200+ Wall Dimmer_ and _HS-WS200+_ at the time of
this writing.

### LED Mode

To change the LED mode, call with the _led_mode_ set to either `normal` or `status` for
normal or status display operation, respectively.

```json
{
  "target_group": "group.example",
  "led_mode": "status"
}
```

### LED colors

To chage one or more LED colors, call with the _colors_ set to a hash consisting of the
LED numbers and the desired color. Valid colors are `White`, `Yellow`, `Green`, `Blue`,
`Off`, `Cyan`, `Magenta`, or `Red`; capitalization is important. Valid LEDs are numbered
`1` through `7`, with `1` on the bottom and `7` on the top of the switch. The following
example changes LEDs 1, 3, and, 6 to red, green and blue, respectively:

```json
{
  "target_group": "group.example",
  "colors": {
    "1": "Red",
    "3": "Green",
    "6": "Blue"
  }
}
```

Note that unlike _blink_ functionality, below, the LED state is maintained individually.
This allows individual LED changes to not change the state of the rest of the group.

### LED blinking

Internal state for blinking is maintained internally within a single parameter in the
switch as a bitmask, with LEDs 1 through 7 corresponding to the least-significant and most-
significant bits, respectively. Math for the bitmask is handled within the script, but a
facility for maintaining state between individual calls does not exist (yet...) As a
result, setting the blink state for an LED will wipe out the states for all other LEDs
unless the existing state is reapplied. The following example will blink LEDs 2, 4, and 7:

```json
{
  "target_group": "group.example",
  "blink": {
    "2": true,
    "4": true,
    "7": true
  }
}
```

### Combinations

Various functions may be combined into a single call. The following example will set
the LEDs to _status_ mode, change the blink frequency to a roughly 100ms on/off time,
change LEDs 6 and 7 to yellow, and blink LEDs 1 and 2 while making LEDs 3-7 solid.

```json
{
  "target_group": "group.example",
  "led_mode": "status",
  "blink_frequency": 2,
  "colors": {
    "6": "Yellow",
    "7": "Yellow"
  },
  "blink": {
    "1": true,
    "2": true
  }
}
```
