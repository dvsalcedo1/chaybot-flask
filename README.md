## Setup
- Setup a virtual environment
- Run `pip install -r requirements.txt`
- [Dev mode]: `flask run` initializes the app locally at `127.0.0.1:5000`

## Formats and standards

### Input format
Requests will be coming in the request body in json format

```
{
    'url': [The article's URL]
    'headline': [The article's title],
    'subhead': [The article's subhead],
    'body': [The article's body] 
}
```

### Processing
Each rule in the ruleset corresponds to one python function,
that takes in a text input and outputs:
```
{
    'ruleCode': [Rule Code, as indicated in the ruleset] type: str, 
    'ruleResult': [PASS or FAIL] type: str,
    'resultDesc': [Optional, default is '', provides notes on reason for FAIL] type: str
}
```  
Dylan's comment: possibly create a NOT APPLICABLE result?


### Output format
Array of all results of rules, and a summary of the tests
This needs to be JSONified (use the `jsonify()` function when outputing the final result array)

```
{
    'details': [
        {
            'ruleCode': 'Head-02',
            'ruleResult': 'PASS',
            'resultDesc': ''
        },
        {
            'ruleCode': 'Head-03',
            'ruleResult': 'FAIL',
            'resultDesc': 'Headline should be in active voice'
        },
    ],
    'summary': {
        'tests_passed': 1,
        'tests_failed': 1
    }
}
```


