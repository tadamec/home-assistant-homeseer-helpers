#HS-WS200+ Switch Helpers

The `ws200.yml` file contains helpers for the HomeSeer 
[HS-WS200+](https://shop.homeseer.com/collections/lighting/products/hsws200)
switch and [HS-WD200+](https://shop.homeseer.com/collections/lighting/products/hswd200)
dimmer.

##DEPRECATED
These scripts should be considered deprecated and will no longer be maintained.
They may be removed in a future version. Future development is being done using
Python scripts in the [python_scripts](../python_scripts/README.md) subdirectory.

##[Usage](#usage)

The various switch modes of the HS-WS200+/HS-WD200+ switches are enabled by setting
Z-Wave configuration items. This means that the Z-Wave _node_id_ -- **not** the
typical _entity_id_ -- must be specified for a given switch. For example,
if switch is named _my_ws200_, there should be two entries in the
`entity_registry.yml` similar to below:

```yaml
zwave.my_wd200:
  config_entry_id:
  name: Home Seer HS-WD200+ Status Dimmer
  platform: zwave
  unique_id: node-1
light.my_wd200_level:
  config_entry_id:
  name: Home Seer HS-WD200+ Status Dimmer Level
  platform: zwave
  unique_id: 1-12345678901234567
```

Setting the dimmer level would typically be accomplished by specifying an
entity ID of `light.my_ws200_level`, while the status features of the HomeSeer
switch would need to be specified by using the integer portion of the
`unique_id` field in the Z-Wave device entry, or `1` in this example.

Changing colors of the LEDs will have no affect unless the switch is already
in status mode, therefore it is advisable to call both `ws200_status_mode` and
`ws200_led_color` any time the LED color is changed. Likewise, setting blink
masks will have no affect if the frequency setting is 0, so calling 
`ws200_blink_frequency` is advisable any time the blink bitmask is set to a
non-zero value via `ws200_led_blink_bitmask`.

## Examples

All examples in this document assume a Home Assistant instance running HTTP on
`localhost` with a port of 8123 bound to the root. No authentication headers
(`x-ha-access`) are supplied. Modify your `curl` commands appropriately.

## Scripts

The following scripts are included.

### `ws200_status_mode`

Enable status mode on an HS-WS200+/HS-WD200+ switch.

#### Parameters

| Key     | Description
| ------- | ---------------------------------------------------------------- |
| node_id | Z-Wave node ID (see [usage](#usage))                             |

#### `curl` Example

Command:
```bash
$ curl -X POST -H 'Content-Type: application/json' \
  -d '{"node_id": 1}' \
  http://assistant.home:8123/api/services/script/ws200_status_mode 
```
Results:
```json
[
    {
        "attributes": {
            "friendly_name": "Activate \"Status mode\" on an HS-WS200+ switch",
            "last_triggered": "2018-08-07T01:15:41.991518+00:00"
        },
        "context": {
            "id": "eb934d39b82346ebbf29f062fe570b58",
            "user_id": null
        },
        "entity_id": "script.ws200_status_mode",
        "last_changed": "2018-08-07T00:24:30.931147+00:00",
        "last_updated": "2018-08-07T01:15:41.996993+00:00",
        "state": "off"
    }
]
```

### `ws200_normal_mode`

Enable normal (dimmer) mode on an HS-WS200+/HS-WD200+ switch.

#### Parameters

| Key     | Description
| ------- | ---------------------------------------------------------------- |
| node_id | Z-Wave node ID (see [usage](#usage))                             |

#### `curl` Example

Command:
```bash
$ curl -X POST -H 'Content-Type: application/json' \
  -d '{"node_id": 1}' \
  http://assistant.home:8123/api/services/script/ws200_normal_mode 
```
Results:
```json
[
    {
        "attributes": {
            "friendly_name": "Activate \"Normal mode\" on an HS-WS200+ switch",
            "last_triggered": "2018-08-07T01:17:53.874664+00:00"
        },
        "context": {
            "id": "05bc09b811464daea9ba20b4d40faa36",
            "user_id": null
        },
        "entity_id": "script.ws200_normal_mode",
        "last_changed": "2018-08-07T00:24:30.930776+00:00",
        "last_updated": "2018-08-07T01:17:53.880215+00:00",
        "state": "off"
    }
]
```

### `ws200_led_color`

Change the color of the specified LED on an HS-WS200+/HS-WD200+ switch.

#### Parameters

| Key     | Description
| ------- | ---------------------------------------------------------------- |
| node_id | Z-Wave node ID (see [usage](#usage))                             |
| led     | LED (1-7) to change; `1` is the bottom, `7` is the top           |
| color   | LED color. See notes below                                       |

#### Notes

Changes to LED colors are stored by the switch when in normal mode, but will
not be reflected until a call to `ws200_status_mode` is made.

Valid colors are _Off_, _Blue_, _Cyan_, _Green_, _Magenta_, _Red_, _White_,
and _Yellow_. 

**WARNING**: Specifying an `led` value lower than 1 or higher than 7 could
(and likely will) cause unexpected behavior in the switch. The script uses the
LED value passed in as an offset for the configuration parameter entry.

#### `curl` Example

Command:
```bash
$ curl -X POST -H 'Content-Type: application/json' \
  -d '{"node_id": 1, "led": 1, "color": "Red"}' \
  http://assistant.home:8123/api/services/script/ws200_led_color
```
Results:
```json
[
    {
        "attributes": {
            "friendly_name": "Change the specified \"Status mode\" LED color on an HS-WS200+ switch",
            "last_triggered": "2018-08-07T01:41:14.140980+00:00"
        },
        "context": {
            "id": "cbf33ed74b464df1b3d57b79d8dbaec3",
            "user_id": null
        },
        "entity_id": "script.ws200_led_color",
        "last_changed": "2018-08-07T00:24:30.932317+00:00",
        "last_updated": "2018-08-07T01:41:14.146437+00:00",
        "state": "off"
    }
]
```

### `ws200_blink_frequency`

Change the blink interval of LEDs on an HS-WS200+HS/HS-WD200+ switch.

#### Parameters

| Key       | Description
| -------   | -------------------------------------------------------------- |
| node_id   | Z-Wave node ID (see [usage](#usage))                           |
| frequency | 0 to disable blinking; 1-255 for 100ms intervals               |

#### Notes

Changing the blink frequency to `0` will disable blinking, regardless of the
setting of the LED blink bit mask. A non-zero value is multiplied by 100
milliseconds to determine the total blink interval. For example, a _frequency_
of `5` will delay for half of a second between on and off, while a delay of
`100` will blink at ten-second intervals.
 
#### `curl` Example

Command:
```bash
$ curl -X POST -H 'Content-Type: application/json' \
  -d '{"node_id": 1, "frequency": 1}' \
  http://assistant.home:8123/api/services/script/ws200_led_color
```
Results:
```json
[
    {
        "attributes": {
            "friendly_name": "Change the blinking LED frequency on an HS-WS200+ switch",
            "last_triggered": "2018-08-07T02:36:30.150067+00:00"
        },
        "context": {
            "id": "3899f59ab989445db53d7587998b3b5e",
            "user_id": null
        },
        "entity_id": "script.ws200_blink_frequency",
        "last_changed": "2018-08-07T00:24:30.931595+00:00",
        "last_updated": "2018-08-07T02:36:30.155136+00:00",
        "state": "off"
    }
]
```

### `ws200_led_blink_bitmask`

Specify LEDs to blink on an HS-WS200+/HS-WD200+ switch.

#### Parameters

| Key       | Description
| -------   | -------------------------------------------------------------- |
| node_id   | Z-Wave node ID (see [usage](#usage))                           |
| bitmask   | One byte, with each bit specifying the LED to blink (see notes)|

#### Notes

Where the individual status LEDs have their own parameter for color
information, a blinking LED is enabled or disabled via a single bit in one
configuration parameter. Each bit from 0 to 6 corresponds to one of the status
LEDs (1 to 7, respectively.) In order to set multiple LEDs blinking, the bit
values must be summed and set, therefore some sort of status must be kept in
order to not wipe out previously set blink modes. For example, blinking LEDs
1, 3 and 6 would require a _bitmask_ parameter of `21`. Once set, LED 1 can
be set to solid by again calling `ws200_led_blink_bitmask` with the bits set
for the remaining LEDs to blink: 3 and 6, for a _bitmask_ value of `20`.

The following values are used in the summation:

 - 1: LED 1 (bottom)
 - 2: LED 2
 - 4: LED 3
 - 8: LED 4
 - 16: LED 5
 - 32: LED 6
 - 64: LED 7 (top)
  
#### `curl` Example

Command:
```bash
$ curl -X POST -H 'Content-Type: application/json' \
  -d '{"node_id": 1, "bitmask": 21}' \
  http://assistant.home:8123/api/services/script/ws200_led_blink_bitmask
```
Results:
```json
[
    {
        "attributes": {
            "friendly_name": "Specify which LEDs to blink in Status mode via bitmask on HS-WS200+ switch",
            "last_triggered": "2018-08-07T02:37:39.482573+00:00"
        },
        "context": {
            "id": "662b77011313443a9d2568f22c1328ca",
            "user_id": null
        },
        "entity_id": "script.ws200_led_blink_bitmask",
        "last_changed": "2018-08-07T00:24:30.931955+00:00",
        "last_updated": "2018-08-07T02:37:39.487918+00:00",
        "state": "off"
    }
]
```
