from __future__ import unicode_literals

import mock

import pytest


@pytest.fixture
def audio():
    return mock.Mock()


@pytest.fixture
def config():
    return {
        'podcast-itunes': {
            'base_url': 'http://itunes.apple.com/',
            'root_directory_name': 'iTunes Store: Top Podcasts',
            'country': 'US',
            'explicit': None,
            'charts': 'podcasts',
            'charts_limit': 20,
            'search_limit': 20,
            'timeout': 10,
            'retries': 3
        },
        'proxy': {}
    }


@pytest.fixture
def backend(config, audio):
    from mopidy_podcast_itunes import backend
    return backend.iTunesPodcastBackend(config, audio)


@pytest.fixture
def library(backend):
    return backend.library