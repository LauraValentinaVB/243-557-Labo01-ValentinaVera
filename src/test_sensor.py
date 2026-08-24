from sensor import Sensor

temperature_sensor = Sensor(
    "Température",
    "°C",
    22.5,
)

distance_sensor = Sensor(
    "Distance",
    "cm",
    35.0,
)

cadence_sensor = Sensor(
    "Cadence",
    "RPM",
    "120",
)

print(temperature_sensor.name,
      temperature_sensor.read(),
      temperature_sensor.unit,)

print( distance_sensor.name,
       distance_sensor.read(),
       distance_sensor.unit,)

distance_sensor.set_value(42.0)

print( cadence_sensor.name,
      cadence_sensor.read(),
      cadence_sensor.unit,)