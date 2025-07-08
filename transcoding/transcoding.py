from ffmpeg import FFmpeg
from transcoding.models import TranscodingInformation
from transcoding.transcoding_options import transcode_options
from utils.filenames import get_resulting_filename

def start_individual_video_transcode(input_location: str, output_location: str, transcoding_info: TranscodingInformation):
    if transcoding_info.two_pass == True:
        ffmpeg = (
            FFmpeg()
            .input(input_location)
            .output(
                output_location,
                transcoding_info.options | {'pass': 1},
                s=transcoding_info.scaling,
            )
        )

        ffmpeg.execute()

        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(input_location)
            .output(
                output_location,
                transcoding_info.options | {'pass': 2},
                s=transcoding_info.scaling,
            )
        )

        ffmpeg.execute()
    else:
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(input_location)
            .output(
                output_location,
                transcoding_info.options,
                s=transcoding_info.scaling,
            )
        )

        ffmpeg.execute()

def start_transcoding_process(input: str):
    for option_name, transcode_option in transcode_options:
        output_object_name = get_resulting_filename(input, option_name)
        start_individual_video_transcode(input, output_object_name, transcode_option)