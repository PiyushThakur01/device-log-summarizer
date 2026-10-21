# Device Log Summarizer
```
python summarize.py device_telemetry.csv -o summary.json   # Sections 1-2
python plot_temps.py summary.json avg_temperature.png      # Section 3
python test_clean_readings.py                              # Section 1 tests
```
Bad CSV rows (missing/invalid temperature, unknown status, empty device_id) are skipped and counted. Devices with average temp > 80.0 are filtered out. Temperature unit assumed °C.
