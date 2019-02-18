from in_service.slack_in_service import SlackInService


class TestCommand:

    def test_slack(self, capsys):
        slack = SlackInService()
        assert slack.connect()
