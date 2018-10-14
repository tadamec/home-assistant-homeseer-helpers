#
# Input parameters
#
# target_group REQUIRED entity_id
#   entity_id of the group of switches to act on.
#
# led_mode OPTIONAL 'normal'|'status'
#   Switches the mode between dimmer level or status display mode.
#
# colors OPTIONAL dictionary
#   Sets the color and the status of specified LEDs. The dictionary key is the
#   position of the LED ('1' is the bottom, '7' is the top) and the value is
#   the color to set (one of 'White', 'Yellow', 'Green', 'Blue', 'Off', 'Cyan',
#   'Magenta', or 'Red'; capitalization is important.)
#
# blink OPTIONAL dictionary
#   Sets the blink status of the specified LEDs. The dictionary key is the
#   position of the LED ('1' is the bottom, '7' is the top) and the value is
#   a boolean (true or false) with true indicating the LED should blink.
#   NOTE: setting blink status on individual LEDs will override the current
#         blink settings. State must be maintained separately.
#
# blink_frequency OPTIONAL byte (0-255)
#   Set the delay value for the blink frequency in multiples of 100ms.
#
###############################################################################

# Helpful constants

#
# Set an individual node's mode
#
def set_led_mode(hass, node_id, mode):
    service_data = {
            'node_id': int(node_id),
            'parameter': 13,
            'value': 'Normal mode'
            }

    if mode == 'status':
        service_data['value'] = 'Status mode';
    elif mode != 'normal':
        logger.warn('set_led_mode called with invalid status mode: {}'.format(mode))
        return

    hass.services.call('zwave', 'set_config_parameter', service_data, False)


#
# Set an individual node's colors for an LED
#
def set_led_color(hass, node_id, led, color):
    VALID_COLORS=['Off', 'Blue', 'Cyan', 'Green', 'Red', 'White', 'Yellow']
    service_data = {
            'node_id': int(node_id),
            'parameter': int(led) + 20,
            'value': 'Off'
            }

    #
    # Maintain sanity
    #
    if color not in VALID_COLORS:
        logger.warn("'{}' is not a valid color.".format(color))
        return
    if led < 1 or led > 7:
        logger.warn("Valid LED values are 1-7. {} is out of range.".format(led))
        return
    
    service_data['value'] = color
    hass.services.call('zwave', 'set_config_parameter', service_data, False)


def set_led_blink(hass, node_id, blink_mask):
    service_data = {
            'node_id': int(node_id),
            'parameter': 31,
            'value': int(blink_mask)
            }
    hass.services.call('zwave', 'set_config_parameter', service_data, False)


def set_blink_frequency(hass, node_id, frequency):
    service_data = {
            'node_id': int(node_id),
            'parameter': 30,
            'value': int(frequency)
            }
    hass.services.call('zwave', 'set_config_parameter', service_data, False)

#
# Grab our parameters
#
target_group = data.get('target_group', 'default_ws_switch')
led_mode = data.get('led_mode', None)
colors = data.get('colors', None)
blink = data.get('blink', None)
blink_frequency = data.get('blink_frequency', None)

#
# Actual work of looping through the group here.
#
group = hass.states.get(target_group)
if group is not None:
    logger.debug("Found group '{}'.".format(target_group))
    for name in group.attributes.get('entity_id'):
        #
        # Make sure we're actually using the correct HomeSeer switches.
        #
        prod = hass.states.get(name).attributes.get('product_name')
        if prod != 'HS-WD200+ Wall Dimmer' and prod != 'HS-WS200+ Wall Switch':
            continue

        node_id = int(hass.states.get(name).attributes.get('node_id'))

        #
        # Do some work here.
        #
        if led_mode is not None:
            set_led_mode(hass, node_id, led_mode)

        if colors is not None:
            for key in colors:
                led = int(key)
                color = colors[key]
                logger.info("Setting color '{}' for LED {}.".format(color, led))
                set_led_color(hass, node_id, led, color)
        
        if blink is not None:
            mask = 0
            for key in blink:
                # We need to assemble a bitmask
                if blink[key]:
                    mask = mask + (1 << (int(key)-1))
            set_led_blink(hass, node_id, mask)

        if blink_frequency is not None:
            set_blink_frequency(hass, node_id, int(blink_frequency) & 255)

else:
    logger.warn("Group '{}' not found.".format(target_group))

