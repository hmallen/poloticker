import configparser
import logging
import os
import sys

from slackclient import SlackClient

config_path = '../../config/config.ini'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def send_slack_alert(channel_id, message, attachments={}, error_message=False):
    alert_return = {'status': True, 'data': None, 'channel': None, 'thread': None}

    try:
        if attachments == {} and error_message == False:
            alert_return['data'] = slack_client.api_call(
                'chat.postMessage',
                channel=channel_id,
                text=message,
                username=slack_bot,
                icon_url=slack_icon
            )

    except Exception as e:
        logger.exception('Exception while sending Slack alert.')
        logger.exception(e)

        alert_return['status'] = False

    finally:
        return alert_return


if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        config.read(config_path)

        slack_token = config['slack']['token']
        slack_channel = config['slack']['channel_testing']
        slack_bot = config['slack']['bot_user']
        slack_icon = config['slack']['bot_icon']

        slack_client = SlackClient(slack_token)

        channel_list = slack_client.api_call('channels.list')
        group_list = slack_client.api_call('groups.list')

        slack_channel_targets = {'alerts': slack_channel}

        for target in slack_channel_targets:
            try:
                logger.debug('channel_list.get(\'ok\'): ' + str(channel_list.get('ok')))
                if channel_list.get('ok'):
                    for chan in channel_list['channels']:
                        logger.debug('chan[\'name\']: ' + chan['name'])
                        if chan['name'] == slack_channel_targets[target]:
                            if target == 'alerts':
                                slack_channel_id = chan['id']

                            break
                    else:
                        logger.error('No valid Slack channel found for alert in channel list.')

                        sys.exit(1)

                else:
                    logger.error('Channel list API call failed.')

                    sys.exit(1)

            except:
                logger.debug('group_list.get(\'ok\'): ' + str(group_list.get('ok')))
                if group_list.get('ok'):
                    for group in group_list['groups']:
                        logger.debug('group[\'name\']: ' + group['name'])
                        if group['name'] == slack_channel_targets[target]:
                            if target == 'alerts':
                                slack_channel_id = group['id']

                            break
                    else:
                        logger.error('No valid Slack channel found for alert in group list.')

                        sys.exit(1)

                else:
                    logger.error('Group list API call failed.')

                    sys.exit(1)

        logger.info('Slack channel for alerts: #' + slack_channel +
                    ' (' + slack_channel_id + ')')

        test_message = 'Hello, world!'

        result = send_slack_alert(slack_channel_id, test_message)

        logger.debug('result: ' + str(result))

    except Exception as e:
        logger.exception(e)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')

        sys.exit()

    finally:
        logger.info('Exiting.')
