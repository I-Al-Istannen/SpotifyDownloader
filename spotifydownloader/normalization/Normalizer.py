import json
import os
import shutil
import subprocess

from ffmpeghelper import ProgressbarHelper
from util import ColorCodes as Color


def normalize(
      tmp_folder: str, file: str, target_i=-16, target_lra=11, target_tp=-1.5
) -> bool:
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    output_json = __first_pass(file, target_i, target_lra, target_tp)

    if "inf" in output_json["input_i"] \
          or "inf" in output_json["input_tp"] \
          or "inf" in output_json["input_lra"] \
          or "inf" in output_json["input_thresh"] \
          or "inf" in output_json["target_offset"]:
        prefix = "\r" + Color.BLUE + "Normalizing" + Color.RESET + " ("
        prefix = prefix \
                 + Color.PURPLE + Color.BOLD + "1st" + Color.RESET + " pass): "

        prefix = prefix + Color.RED + Color.BOLD + \
                 "Unsuccessful, measured values out of bounds. Does the file" \
                 " contain audio?" + Color.RESET
        print(prefix)
        return False

    __second_pass(tmp_folder, file, output_json, target_i, target_lra,
                  target_tp)

    return True


def __first_pass(input_file, target_i, target_lra, target_tp) -> dict:
    """Performs the first pass for the loudnorm filter"""

    filter_arguments = "loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}" \
                       ":print_format=json" \
        .format(
          target_i=target_i, target_tp=target_tp, target_lra=target_lra)

    ffmpeg_args = [
        "ffmpeg", "-i", input_file,
        "-af", filter_arguments,
        "-codec:a", "libmp3lame",  # nice codec
        "-q:a", "2",  # quality
        "-f", "null", "-"
    ]

    prefix = Color.BLUE + "Normalizing" + Color.RESET + " ("
    prefix = prefix + Color.PURPLE + Color.BOLD + "1st" + Color.RESET + " pass)"

    end = "\r{prefix}: " + Color.GREEN + "Done" + Color.RESET

    first_pass_output = ProgressbarHelper.execute_with_bar(
          ffmpeg_args, prefix, end)
          
    first_pass_output = first_pass_output[-12:]

    first_pass_output = "\n".join(first_pass_output)
    
    return json.loads(first_pass_output)


def __second_pass(
      tmp_folder: str, input_file: str, output_json: dict, target_i: float,
      target_lra: float, target_tp: float):
    """The second pass of the loudnorm filter"""
    filter_arguments = [
        "loudnorm=I={target_i}:TP={target_tp}:LRA={target_lra}",
        "measured_I={measured_i}:measured_TP={measured_tp}"
        + ":measured_LRA={measured_lra}",
        "measured_thresh={measured_thresh}:offset={measured_offset}",
        "linear=true:print_format=summary"
    ]

    filter_arguments_string = ":".join(filter_arguments) \
        .format(
          target_i=target_i, target_lra=target_lra, target_tp=target_tp,
          measured_i=output_json["input_i"],
          measured_tp=output_json["input_tp"],
          measured_lra=output_json["input_lra"],
          measured_thresh=output_json["input_thresh"],
          measured_offset=output_json["target_offset"])

    resulting_path = os.path.join(tmp_folder, os.path.basename(input_file))
    ffmpeg_second_pass_args = [
        "ffmpeg", "-y", "-i", input_file,
        "-af", filter_arguments_string,
        resulting_path
    ]

    try:
        prefix = Color.BLUE + "Normalizing" + Color.RESET + " ("
        prefix = prefix + Color.PURPLE + Color.BOLD + "2nd"
        prefix = prefix + Color.RESET + " pass)"

        end = "\r" + Color.BLUE + "Normalizing: " + Color.GREEN + "Done."
        end = end + Color.RESET + "\n"

        ProgressbarHelper.execute_with_bar(ffmpeg_second_pass_args, prefix, end)

        if os.path.exists(input_file):
            os.remove(input_file)
        shutil.move(resulting_path, input_file)
    except subprocess.CalledProcessError as e:
        raise e
