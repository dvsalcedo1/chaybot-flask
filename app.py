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
        pf.head_09(input_content,'headline'),
        pf.head_10(input_content,'headline'),
        pf.head_11(input_content,'headline'),
        pf.head_12(input_content,'headline'),
        pf.subhead_01(input_content,'subhead'),
        pf.subhead_06(input_content,'subhead'),
        pf.dateline_03(input_content,'body'),
        pf.url_01(input_content,'url'),
        pf.url_04(input_content,'url'),
        pf.url_06(input_content,'url')
    ]

    summary = {
        'tests_passed': len([i['ruleResult'] for i in details if i['ruleResult']=='PASS']),
        'tests_failed': len([i['ruleResult'] for i in details if i['ruleResult']=='FAIL'])
    }

    return jsonify({'details': details, 'summary': summary})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
