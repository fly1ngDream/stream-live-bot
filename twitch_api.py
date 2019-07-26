from class_utils import default_property, default_getter, DefaultRepresentationMixin
from dotenv import load_dotenv

import json
import requests
import os


load_dotenv()


class UsernameError(Exception):
    pass


class TwitchAPI(DefaultRepresentationMixin):
    _url = 'https://api.twitch.tv/helix'

    url = default_getter('url')
    client_id = default_property('client_id')

    def __init__(self, client_id):
        self.client_id = client_id

    def get_user_id_by_username(self, username):
        '''
        Gets streamer's user id by username
        '''
        headers = {
            'Client-ID': self.client_id,
        }
        users_url = f'{self.url}/users?login={username}'
        user_data = json.loads(
            requests.get(
                users_url,
                headers=headers
            ).text
        ).get('data')

        user_id = -1

        if user_data == []:
            raise UsernameError('Invalid username')
        else:
            user_id = int(user_data[0].get('id'))
            return user_id

    def is_stream_online(self, username):
        '''
        Checks if stream is online
        '''
        headers = {
            'Client-ID': self.client_id,
        }
        user_id = self.get_user_id_by_username(username)
        streams_url = f'{self.url}/streams?user_id={user_id}'

        response_json = json.loads(
            requests.get(
                url=streams_url,
                headers=headers
            ).text
        )

        streams_data = response_json.get('data')

        return True if streams_data != [] else False

    def subscribe_for_stream_changes(self, username):
        '''
        Subscribes for stream changes using webhook
        '''
        headers = {
            'Client-ID': self.client_id,
        }

        user_id = self.get_user_id_by_username(username)

        webhooks_hub_url = f'{self.url}/webhooks/hub'
        ip = os.getenv('IP')
        hub_data = {
            'hub.callback': f'http://{ip}:8000/stream_changed',
            'hub.mode': 'subscribe',
            'hub.topic': f'{self.url}/streams?user_id={user_id}',
            'hub.lease_seconds': 864000,
        }
        requests.post(
            webhooks_hub_url,
            json=hub_data,
            headers=headers,
        )
