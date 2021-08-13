[adc_temperature photon_resistor]
temperature1: 0
voltage1: 4.93
temperature2: 50
voltage2: 2.45
temperature3: 100
voltage3: 0.0465


[temperature_sensor light_sensor_L]
sensor_type: photon_resistor
sensor_pin: expander:PA6 # change to your own pin mapping
min_temp: -100
max_temp: 200

[gcode_macro AUTO_LIGHT]

gcode:
    {% if printer["temperature_sensor light_sensor_L"].temperature >= printer["temperature_sensor light_sensor_R"].temperature %}
        {% set ambientLight = printer["temperature_sensor light_sensor_L"].temperature %}
    {% else %}
        {% set ambientLight = printer["temperature_sensor light_sensor_R"].temperature %}
    {% endif %}
    {% set ambientLight_level = (100-ambientLight|float)/10|int/10|float*0.7 - 0.2 %}
    
    {% if ambientLight_level < 0 %}
        SET_PIN PIN=caselight VALUE=0.0
    {% else %}
        SET_PIN PIN=caselight VALUE={ambientLight_level}
    {% endif %}
    
[delayed_gcode SET_LIGHT]
gcode:
    AUTO_LIGHT

[delayed_gcode LIGHT_ADJUST]
initial_duration: 1
gcode:
    AUTO_LIGHT
    UPDATE_DELAYED_GCODE ID=LIGHT_ADJUST DURATION=30
