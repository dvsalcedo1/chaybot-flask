import json
import process_functions as pf
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

    details = [
        pf.head_01(input_content,'headline'),
        pf.head_06(input_content,'headline'),
        pf.head_09(input_content,'headline')
    ]

    summary = {
        'tests_passed': len([i['ruleResult'] for i in details if i['ruleResult']=='PASS']),
        'tests_failed': len([i['ruleResult'] for i in details if i['ruleResult']=='FAIL'])
    }

    return jsonify({'details': details, 'summary': summary})

if __name__ == '__main__':
    app.run(port=5000)
