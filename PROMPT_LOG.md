# PROMPT_LOG

## Initial prompt
"Write a Python script that loads `summary.json` (a list of objects with `device_id`, `avg_temperature`, `total_records`, `error_count`) and generates a bar chart of average temperature per device using matplotlib. Save it as a PNG."

## Bug in the first attempt
The first version was a bare `plt.bar(...)` + `savefig`: no title, no axis labels, no value labels, no `tight_layout()` (labels risk being clipped/overlapping with more devices), and no error handling for a missing or empty JSON file.

## Follow-up prompt
"Add a title, x/y axis labels with units, value labels on top of each bar, rotate x tick labels 45° so they don't overlap, use tight_layout, save at 150 dpi, and exit with a clear message if the JSON file is missing, invalid or empty."

## My review
I read the output, checked the data keys matched my JSON, set the y-limit with headroom so bar labels aren't cut off, and switched to the `Agg` backend so it runs headless.
