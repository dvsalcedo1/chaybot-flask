### Input format
Requests will be coming in the request body in json format

```
{
    'url': [The article's URL]
    'title': [The article's title],
    'body': [The article's body] 
}
```

### Processing
Each rule in the ruleset corresponds to one python function,
that takes in a text input and outputs:
```
{
    'ruleCode': [Rule Code, as indicated in the ruleset],
    'ruleResult': [PASS or FAIL],
    'resultDesc': [Optional, default is '', provides notes on reason for FAIL]
}
```  

### Output format
