import json
from rule_list import agg_details
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/basictests",methods=['POST'])
def summarize_rules():
    """
    request.data = {
        'url': [The article's URL]
        'headline': [The article's title],
        'subhead': [The article's subhead],
        'body': [The article's body] 
    }
    """
    input_content = json.loads(request.data)

    details = agg_details(input_content)

    summary = {
        'tests_passed': len([i['ruleResult'] for i in details if i['ruleResult']=='PASS']),
        'tests_failed': len([i['ruleResult'] for i in details if i['ruleResult']=='FAIL'])
    }

    return jsonify({'details': details, 'summary': summary})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
