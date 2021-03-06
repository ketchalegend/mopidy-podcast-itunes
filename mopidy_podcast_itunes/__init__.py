from __future__ import unicode_literals

import os

from mopidy import config, ext, httpclient

__version__ = '2.0.0'

CHARTS = ['podcasts', 'audioPodcasts', 'videoPodcasts']

COUNTRIES = [
    'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR',
    'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE',
    'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ',
    'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA', 'CC', 'CD',
    'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR',
    'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM',
    'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI',
    'FJ', 'FK', 'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF',
    'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS',
    'GT', 'GU', 'GW', 'GY', 'HK', 'HM', 'HN', 'HR', 'HT', 'HU',
    'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT',
    'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN',
    'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK',
    'LR', 'LS', 'LT', 'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME',
    'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ',
    'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA',
    'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU',
    'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM',
    'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS',
    'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI',
    'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST', 'SV',
    'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK',
    'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA',
    'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI',
    'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW'
]

EXPLICIT = ('Yes', 'No')  # since config.Boolean has no "optional"

MAX_LIMIT = 200  # absolute limit specified by iTunes Store API


class Extension(ext.Extension):

    dist_name = 'Mopidy-Podcast-iTunes'
    ext_name = 'podcast-itunes'
    version = __version__

    def get_default_config(self):
        return config.read(os.path.join(os.path.dirname(__file__), 'ext.conf'))

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema.update(
            base_url=config.String(),
            country=config.String(choices=COUNTRIES),
            explicit=config.String(choices=EXPLICIT, optional=True),
            charts=config.String(choices=CHARTS),
            charts_limit=config.Integer(
                minimum=1, maximum=MAX_LIMIT, optional=True
            ),
            search_limit=config.Integer(
                minimum=1, maximum=MAX_LIMIT, optional=True
            ),
            timeout=config.Integer(minimum=1, optional=True),
            retries=config.Integer(minimum=0),
            # no longer used
            charts_format=config.Deprecated(),
            episode_format=config.Deprecated(),
            genre_format=config.Deprecated(),
            podcast_format=config.Deprecated(),
            root_genre_id=config.Deprecated(),
            root_name=config.Deprecated()
        )
        return schema

    def setup(self, registry):
        from .backend import iTunesPodcastBackend
        registry.add('backend', iTunesPodcastBackend)

    @classmethod
    def get_requests_session(cls, config):
        import requests

        proxy = httpclient.format_proxy(config['proxy'])
        user_agent_string = '%s/%s' % (cls.dist_name, cls.version)
        user_agent = httpclient.format_user_agent(user_agent_string)

        session = requests.Session()
        session.proxies.update({'http': proxy, 'https': proxy})
        session.headers.update({'user-agent': user_agent})
        return session
