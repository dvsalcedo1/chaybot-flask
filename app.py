import json
import subprocess
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

@app.route('/webhook', methods=['POST'])
def webhook():
    # You can add authentication if needed
    if request.method == 'POST':
        # Trigger a git pull
        repo_path = '.'  # Update this to your repo
        try:
            subprocess.run(['git', '-C', repo_path, 'pull'], check=True)
            # subprocess.run(['sudo', 'systemctl', 'restart', 'app'], check=True)
            return jsonify({'status': 'success'}), 200
        except subprocess.CalledProcessError as e:
            return jsonify({'status': 'failed', 'error': str(e)}), 500
    return jsonify({'status': 'invalid request'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
