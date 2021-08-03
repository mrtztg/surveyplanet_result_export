import argparse
import re


class Validator(object):

    def __init__(self, pattern, argument_name, example):
        self._pattern = re.compile(pattern)
        self._err_message = (f"\n{argument_name} is not in correct format. "
                             f"It must be something like this:\n{example}")

    def __call__(self, value):
        if not self._pattern.match(value):
            raise argparse.ArgumentTypeError(
                # "Argument has to match '{}'".format(self._pattern.pattern))
                self._err_message
            )

        return value


class ArgsParser:
    acc_username, acc_password, output_verbose, __input_urls_file = None, None, None, None

    def __init__(self):
        url_validator = Validator('.*app\\.surveyplanet\\.com/participants/.{10,}',
                                  "Question participants url",
                                  "https://app.surveyplanet.com/participants/61a50e9876f392908f6c10a8")
        arg_parser = argparse.ArgumentParser(
            description="Export survey results from SurveyPlanet.com.")
        arg_parser.add_argument('-u', '--username', type=str, help='Account email/username')
        arg_parser.add_argument('-p', '--password', type=str, help='Account password')
        arg_parser.add_argument('-q', '--question_participants_url', type=url_validator,
                                help='participants url. ex: https://app.surveyplanet.com/'
                                     'participants/61a50e9876f392908f6c10a8')
        arg_parser.add_argument('--display', help='Display the browser to user',
                                action='store_true')
        arg_parser.add_argument('-v', '--verbose', help='Increase output verbosity',
                                action='store_true')

        args = arg_parser.parse_args()
        self.acc_username = args.username
        self.acc_password = args.password
        self.output_verbose = args.verbose
        self.question_participants_url = args.question_participants_url
        self.display_browser = args.display