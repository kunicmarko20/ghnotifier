#!/usr/bin/env python3
import gi
import requests

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk, GLib, Notify
from config import Config


class Notifier:

    GITHUB_API_NOTIFICATIONS = 'https://api.github.com/notifications'

    def __init__(self, indicator):
        self.indicator = indicator
        self.config = Config()
        self.notified = []

        Notify.init(indicator.INDICATOR_ID)

    def notify(self):
        notifications = self.get_notifications()

        for notification in notifications:
            if not self.is_notified(notification['id']):
                Notify.Notification.new(
                    "<b>" + notification['subject']['title'] + " @ " + notification['repository']['name'] + "</b>"
                ).show()
                self.notified.append(notification['id'])

        self.indicator.update_label(str(len(notifications)))

        GLib.timeout_add_seconds(int(self.config.get('refreshTime')), self.notify)

    def get_notifications(self):
        response = requests.get(
            self.GITHUB_API_NOTIFICATIONS,
            headers={
                'Authorization': 'token ' + self.config.get('accessToken'),
                'User-Agent': 'my app'
            }
        )

        return response.json()

    def is_notified(self, identifier):
        return identifier in self.notified

    @staticmethod
    def stop():
        Notify.uninit()
