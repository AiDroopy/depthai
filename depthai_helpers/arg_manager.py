import os
import argparse
from pathlib import Path
import cv2

try:
    import argcomplete
except ImportError:
    raise ImportError('\033[1;5;31m argcomplete module not found, run: python3 install_requirements.py \033[0m')


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def check_range(min_val, max_val):
    def check_fn(value):
        ivalue = int(value)
        if min_val <= ivalue <= max_val:
            return ivalue
        else:
            raise argparse.ArgumentTypeError(
                "{} is an invalid int value, must be in range {}..{}".format(value, min_val, max_val)
            )

    return check_fn


_stream_choices = ("nn_input", "color", "left", "right", "depth", "disparity", "disparity_color", "rectified_left", "rectified_right")
color_maps = list(map(lambda name: name[len("COLORMAP_"):], filter(lambda name: name.startswith("COLORMAP_"), vars(cv2))))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-cam', '--camera', choices=["left", "right", "color"], default="color", help="Use one of DepthAI cameras for inference (conflicts with -vid)")
    parser.add_argument('-vid', '--video', type=str,
                        help="Path to video file to be used for inference (conflicts with -cam)")
    parser.add_argument('-hq', '--high_quality', action="store_true", default=False,
                        help="Low quality visualization - uses resized frames")
    parser.add_argument('-dd', '--disable_depth', action="store_true", help="Disable depth information")
    parser.add_argument('-cnnp', '--cnn_path', type=Path, help="Path to cnn model directory to be run")
    parser.add_argument("-cnn", "--cnn_model", default="mobilenet-ssd", type=str,
                        help="Cnn model to run on DepthAI")
    parser.add_argument('-sh', '--shaves', default=13, type=int,
                        help="Name of the nn to be run from default depthai repository")
    parser.add_argument('-cnn_size', '--cnn_input_size', default=None, type=str,
                        help="Neural network input dimensions, in \"WxH\" format, e.g. \"544x320\"")
    parser.add_argument("-rgbr", "--rgb_resolution", default=1080, type=int, choices=[1080, 2160, 3040],
                        help="RGB cam res height: (1920x)1080, (3840x)2160 or (4056x)3040. Default: %(default)s")
    parser.add_argument("-rgbf", "--rgb_fps", default=30.0, type=float,
                        help="RGB cam fps: max 118.0 for H:1080, max 42.0 for H:2160. Default: %(default)s")
    parser.add_argument("-dct", "--disparity_confidence_threshold", default=200, type=check_range(0, 255),
                        help="Disparity confidence threshold, used for depth measurement. Default: %(default)s")
    parser.add_argument("-med", "--stereo_median_size", default=7, type=int, choices=[0, 3, 5, 7],
                        help="Disparity / depth median filter kernel size (N x N) . 0 = filtering disabled. Default: %(default)s")
    parser.add_argument('-lrc', '--stereo_lr_check', action="store_true",
                        help="Enable stereo 'Left-Right check' feature.")
    parser.add_argument('-ext', '--extended_disparity', action="store_true",
                        help="Enable stereo 'Extended Disparity' feature.")
    parser.add_argument('-sub', '--subpixel', action="store_true",
                        help="Enable stereo 'Subpixel' feature.")
    parser.add_argument("-ff", "--full_fov_nn", default=False, action="store_true",
                        help="Full RGB FOV for NN, not keeping the aspect ratio")
    parser.add_argument("-scale", "--scale", default=1.0, type=float,
                        help="Scale factor for the output window. Default: %(default)s")
    parser.add_argument("-cm", "--color_map", default="JET", choices=color_maps, help="Change color map used to apply colors to depth/disparity frames. Default: %(default)s")
    parser.add_argument("-maxd", "--max_depth", default=10000, type=int,
                        help="Maximum depth distance for spatial coordinates in mm. Default: %(default)s")
    parser.add_argument("-mind", "--min_depth", default=100, type=int,
                        help="Minimum depth distance for spatial coordinates in mm. Default: %(default)s")
    parser.add_argument('-sbb', '--spatial_bounding_box', action="store_true",
                        help="Display spatial bounding box (ROI) when displaying spatial information. The Z coordinate get's calculated from the ROI (average)")
    parser.add_argument("-sbb_sf", "--sbb_scale_factor", default=0.3, type=float,
                        help="Spatial bounding box scale factor. Sometimes lower scale factor can give better depth (Z) result. Default: %(default)s")
    parser.add_argument('-s', '--show', default=[], nargs="+", choices=_stream_choices, help="Choose which previews to show. Default: %(default)s")
    parser.add_argument('--report', nargs="+", default=[], choices=["temp", "cpu", "memory"], help="Display device utilization data")
    parser.add_argument('--report_file', help="Save report data to specified target file in CSV format")
    parser.add_argument('-sync', '--sync', action="store_true",
                        help="Enable NN/camera synchronization. If enabled, camera source will be from the NN's passthrough attribute")
    parser.add_argument("-monor", "--mono_resolution", default=400, type=int, choices=[400,720,800],
                        help="Mono cam res height: (1280x)720, (1280x)800 or (640x)400. Default: %(default)s")
    parser.add_argument("-monof", "--mono_fps", default=30.0, type=float,
                        help="Mono cam fps: max 60.0 for H:720 or H:800, max 120.0 for H:400. Default: %(default)s")
    return parser.parse_args()
