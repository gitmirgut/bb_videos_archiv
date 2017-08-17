#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

# Please notice license of module:
# https://github.com/BioroboticsLab/bb_binary/blob/master/python/bb_binary/repository.py#L41
"""This module contains functions to search for videos of the beesbook project."""
import ast
import datetime
import os

import bb_binary.parsing as bbb_p
import bb_videos_iterator.helpers as helpers


class Video_Archiv(object):
    # This module is an adaption of
    # https://github.com/BioroboticsLab/bb_binary/blob/master/python/bb_binary/repository.py#L41
    # for videos
    """The Video Archiv class manages multiple video files of the beesbook project."""

    def __init__(self, year, root_dir=None, config=None):
        """Initialize a video archiv for the `year` with the `root_dir`.

        The format of the file video_archiv must be declared in the `config`.

        Args:
            year (string): year of the video archiv.
            root_dir (string): Path of the root dir of the archiv from the `year` of observation.
            config: Configuration which holds the various information about the filestructure.
        """
        if config is None:
            self.config = helpers.get_default_config()
        else:
            self.config = config

        if root_dir is not None:
            self.root_dir = root_dir
        else:
            self.root_dir = self.config[year]['ROOT_DIR']

        self.valid_cam_ids = ast.literal_eval(self.config[year]['CAM_IDS'])
        self.dir_format = self.config[year]['DIR_FORMAT']
        self.video_ext = self.config[year]['VIDEO_EXT']

    def _path_for_dt_cam(self, ts, cam_id, abs=False):
        """Return the directory path of videos to the given timestamp.

        Args:
            ts (datetime): Timestamp to search for.
            cam_id (int): Camera id to search for.
            abs (bool): If *True* returns the absolute path to the directory.

        Returns:
            string: path of the directory
        """
        dt = bbb_p.to_datetime(ts)
        if cam_id not in self.valid_cam_ids:
            raise ValueError("Unknown camera id {cam_id}.".format(cam_id=cam_id))
        # TODO(gitmirgut) is this possible for videos of 2015? Mabye the day folders are in Berlin
        # style and not in ISO8601 style
        format = self.dir_format.format(dt=dt, cam_id=cam_id)
        if abs:
            return os.path.join(self.root_dir, format)
        else:
            return format

    def _paths_for_dt_cam(self, ts, cam_id=None, abs=False):
        """Return the directory paths of videos to the given timestamp.

        Args:
            ts (datetime): Timestamp to search for.
            cam_id (int): Camera id to search for, if None the function search for all cam ids.
            abs (bool): If *True* returns the absolute path to the directory.

        Returns:
            list(string): paths of the directories for the given timestamp.
        """
        paths = []
        if cam_id is None:
            for cam_id in self.valid_cam_ids:
                paths.append(self._path_for_dt_cam(ts, cam_id, abs))
        else:
            paths.append(self._path_for_dt_cam(ts, cam_id, abs))
        return paths

    def _all_videos_in(self, path):
        assert type(path) == str

        if not os.path.isdir(path):
            return []
        return [f for f in os.listdir(path) if f.lower().endswith(self.video_ext)]

    def find_by_ts(self, ts, cam_id=None):
        """Return all video file paths that belong to the `ts`.

        Args:
            ts (datetime): timestamp to search for.
            cam_id (int): camera id to search for.

        Returns:
            list(string): paths of video files.
        """
        # TODO(gitmirgut): Check if 20min is to big and if its also needed for time near 23:59..
        dt = bbb_p.to_datetime(ts)
        paths = self._paths_for_dt_cam(dt, cam_id, abs=True)

        # check if time is near 0 hour, to get paths from the day before.
        time_delta = datetime.timedelta(minutes=20)
        shift_time = dt - time_delta
        if shift_time.day != dt.day:
            # TODO(gitmirgut): Change it to append.
            paths = paths + self._paths_for_dt_cam(shift_time, cam_id, abs=True)
        video_paths = []
        for path in paths:
            fnames = self._all_videos_in(path)
            fname_parts = [(f, bbb_p.parse_video_fname(f)) for f in fnames]
            for fname, (camId, begin, end) in fname_parts:
                if begin <= dt < end:
                    video_paths.append(os.path.join(path, fname))
                    # TODO(gitmirgut): insert breake
        return video_paths

    def get_abs_path_by_name(self, name):
        """Return the absolute path of the video.

        Args:
            name (str): Name of the video.

        Returns: Absolute path of the video if it exists otherwise None.
        """
        cam_id, ts_start, __ = bbb_p.parse_video_fname(name)
        path = self._path_for_dt_cam(ts_start, cam_id, True)
        file_path = os.path.join(path, name)
        if os.path.exists(file_path):
            return file_path
        else:
            return None

    def find_closest_videos(self, ts, cam_id, abs=False):
        """Return closest videos to the given timestamp.

        Args:
            ts (datetime): timestamp to search for.
            cam_id (int): camera id to search for.

        Returns:
            list(string): paths of video files.
        """
        # TODO(gitmirgut): Check if 20min is to big and if its also needed for time near 23:59..
        dt = bbb_p.to_datetime(ts)

        paths = [self._path_for_dt_cam(dt, cam_id, abs=True)]

        # check if time is near 0 hour, to get paths from the day before.
        time_delta = datetime.timedelta(minutes=20)
        shift_time = dt - time_delta
        print('time')
        print(dt)
        print(shift_time)
        if shift_time.day != dt.day:
            paths.append(self._path_for_dt_cam(shift_time, cam_id, abs))

        shift_time = dt + time_delta
        if shift_time.day != dt.day:
            paths.append(self._path_for_dt_cam(shift_time, cam_id, abs))

        paths.sort()
        prev = None
        succ = None
        for path in paths:
            fnames = self._all_videos_in(path)
            fnames.sort()
            fnames_parts = [(f, bbb_p.parse_video_fname(f)) for f in fnames]
            for fname, (camId, begin, end) in fnames_parts:
                if begin <= ts < end:
                    ret = fname
                    if abs:
                        return [os.path.join(path, ret)]
                    else:
                        return ret
                elif end < ts:
                    prev = fname
                elif ts < begin:
                    succ = fname
                    if abs:
                        return [os.path.join(path, prev), os.path.join(path, succ)]
                    else:
                        return [prev, succ]
