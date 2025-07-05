from typing import List

from transcoding.models import TranscodingInformation


options: List[TranscodingInformation] = [
    {
        'scaling': '360:-1',
        'options': {
            'c:v': 'libx264',
            'c:a': 'aac',
            'b:a': '128k',
            'preset': 'slow',
            'movflags': '+faststart'
        },
        'two_pass': False,
        'options_second_pass': {}
    },
    {
        'scaling': '480:-1',
        'options': {
            'c:v': 'libx264',
            'c:a': 'aac',
            'b:a': '128k',
            'preset': 'slow',
            'movflags': '+faststart'
        },
        'two_pass': False,
        'options_second_pass': {}
    },
    {
        'scaling': '720:-1',
        'options': {
            'c:v': 'libx264',
            'c:a': 'aac',
            'b:a': '128k',
            'preset': 'slow',
            'movflags': '+faststart'
        },
        'two_pass': False,
        'options_second_pass': {}
    },
    {
        'scaling': '1080:-1',
        'options': {
            'c:v': 'libx264',
            'c:a': 'aac',
            'b:a': '256k',
            'preset': 'slow',
            'movflags': '+faststart'
        },
        'two_pass': False,
        'options_second_pass': {}
    },
    {
        'scaling': '1080:-1',
        'options': {
            'c:v': 'libvpx-vp9',
            'b:v': '0',
            'crf': '30',
            'an': None,
            'f': 'null',
        },
        'two_pass': True,
        'options_second_pass': {
            'c:v': 'libvpx-vp9',
            'b:v': '0',
            'crf': '30',
            'c:a': 'libopus',
        }
    }
]