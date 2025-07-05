from ffmpeg import FFmpeg
from transcoding.models import TranscodingInformation

def start_transcoding_process(location: str, output_location: str, transcoding_info: TranscodingInformation):
    if transcoding_info.two_pass == True:
        ffmpeg = (
            FFmpeg()
            .input(location)
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
            .input(location)
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
            .input(location)
            .output(
                output_location,
                transcoding_info.options,
                s=transcoding_info.scaling,
            )
        )

        ffmpeg.execute()