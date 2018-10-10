'''
@author : breddy
'''
import json
import unicodedata
from flask import Flask
from jira import JIRAError
from jira_api.jira_base import JiraBase
from jira_api.settings import Settings

app = Flask(__name__)
jira_base = JiraBase()


def ignore_ascii(field):
    if isinstance(field, unicode):
        return unicodedata.normalize('NFKD', field).encode('ascii', 'ignore')
    else:
        return field


@app.route('/issue/fields/<issue_id>', methods=['GET'])
def get_issue_fields(issue_id):
    try:
        jira_base.get_connection()
        fields = jira_base.get_issue_fields(issue_id)
        response = dict()
        response['issue_id'] = issue_id
        response['status'] = ignore_ascii(fields.status.name)
        response['assignee'] = ignore_ascii(fields.assignee.name)
        response['summary'] = ignore_ascii(fields.summary)
        response['priority'] = ignore_ascii(fields.priority.name)
        response['reporter'] = ignore_ascii(fields.reporter.name)
        response['url'] = "%s://%s:%s/browse/%s" % (Settings.JIRA_PROTOCOL, Settings.JIRA_HOST_NAME, Settings.JIRA_PORT,
                                                    issue_id)
        return app.response_class(response=json.dumps(response), status=200, mimetype='application/json')
    except JIRAError as e:
        return app.response_class(response=json.dumps({"error": e.text}), status=e.status_code,
                                  mimetype='application/json')

if __name__ == '__main__':
    app.run(port=Settings.APP_PORT, debug=Settings.APP_DEBUG)

