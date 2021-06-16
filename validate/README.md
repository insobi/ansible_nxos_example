# JSON Validator
This is a simple validator for specific value in JSON file.
<br><br>

# How to run

```
# python validation.py -r [RULE_FILE] -s [SOURCE_FILE] -o [OUTPUT_FILE]

python validation.py --rule rule1.json --source example1.json --output output1.json

python validation.py --rule rule2.json --source example2.json --output output2.json
```
<br>

# Sample Test
This is a source file to validate.
```
[
    {
        "hostname": "N3K-C31108PC-V-1",
        "version": "9.3(6)"
    },
    {
        "hostname": "N3K-C31108PC-V-2",
        "version": "9.4"
    }
]
```

Next, this is a rule file.
```
{
    "rule_name":   "version check",
    "index":       "hostname",
    "valid_key":   "version",
    "valid_value": "9.3(6)",
    "condition":   "eq",
    "if_valid":    "SUCCESS",
    "if_invalid":  "FAIL"
}
```

As a results, you can see below file created.
```
[
    {
        "hostname": "N3K-C31108PC-V-1",
        "version": "9.3(6)",
        "valid": "SUCCESS"
    },
    {
        "hostname": "N3K-C31108PC-V-2",
        "version": "9.4",
        "valid": "FAIL"
    }
]
```

<br>

# Reference
- https://hackersandslackers.com/extract-data-from-complex-json-python/