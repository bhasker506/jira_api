'''
@author : breddy
'''
from jira import JIRA
from jira_api.settings import Settings


class JiraBase(object):

    _jira = None

    def __init__(self, protocol='http', host_name=Settings.JIRA_IP, port=Settings.JIRA_PORT,
                 usr_name=Settings.JIRA_USER_NAME, passwd=Settings.JIRA_PASSWD):
        self.url = protocol+'://'+host_name+':'+port
        self.usr_name = usr_name
        self.passwd = passwd

    def get_connection(self):
        if self._jira is None:
            print 'Creating jira Connection....'
            options = {'server': self.url}
            self._jira = JIRA(options, basic_auth=(self.usr_name, self.passwd))

    def get_issue_fields(self, issue_id):
        ''' Get Issue Fields

        :param string issue_id: JIRA id
        :return:
        '''
        issue = self._jira.issue(issue_id)
        return issue.fields

