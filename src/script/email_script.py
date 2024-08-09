import argparse
import traceback

from src.manager.mail_process_manager import MailProcessManager

script_parser = argparse.ArgumentParser(
    description='Script to execute the email functionality like fetching and filtering')
script_parser.add_argument('--action',
                           action="store",
                           type=str,
                           required=True,
                           choices=('fetch', 'filter'),
                           help='script action')
script_parser.add_argument("--name",
                           action="store",
                           type=str,
                           required=False,
                           help='filter name')
args = script_parser.parse_args()


def fetch_email_action():
    """
    method to fetch the emails from the mailbox and store in the database
    :return:
    """

    try:
        mail_process_manager_obj = MailProcessManager()
        messages = mail_process_manager_obj.get_latest_email()
        failure_list = mail_process_manager_obj.store_email_details(messages)
        print(f"Failure list: {failure_list}")
    except Exception as ex:
        print(traceback.format_exc())
        print(f"Exception {ex} occurred while fetching the email")
        raise ex


def filter_email_action():
    """
    function to filter the email based on the given filter
    :return:
    """
    try:
        if not args.name:
            script_parser.error("--name is required when --action is 'filter'")

        mail_process_manager_obj = MailProcessManager()
        mail_process_manager_obj.execute_rule_by_rule_name(args.name)
    except Exception as ex:
        print(f"Exception {ex} occurred while applying filter")
        raise ex


def execute():
    try:
        action_mapper = {
            "fetch": fetch_email_action,
            "filter": filter_email_action
        }

        action_mapper.get(args.action)()
    except Exception as ex:
        print(f"Exception while executing {args.action} action: {ex}")


if __name__ == "__main__":
    try:
        execute()
    except (IOError, Exception):
        print('Process already running and locked by %s' % lock_path)
