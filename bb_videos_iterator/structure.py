import ast
import datetime
import os

import bb_videos_iterator.helpers as helpers
import bb_binary.parsing as bbb_p


class Directory_Tree_Structure(object):

    def __init__(self, root_dir, year='2016', config=None):
        if config is None:
            self.config = helpers.get_default_config()
        else:
            self.config = config
        self.root_dir = root_dir
        self.valid_cam_ids = ast.literal_eval(self.config[year]['CAM_IDS'])
        self.dir_format = self.config[year]['DIR_FORMAT']
        self.video_ext = self.config[year]['VIDEO_EXT']

    # TODO(gitmirgut): Noch Lösung überlegen was mit Files um 0 Uhr ist.
    def _path_for_dt_cam(self, time, cam_id, abs=False):
        dt = bbb_p.to_datetime(time)
        if cam_id not in self.valid_cam_ids:
            raise ValueError("Unknown camera id {cam_id}.".format(cam_id=cam_id))
        format = self.dir_format.format(dt=dt, cam_id=cam_id)
        if abs:
            return os.path.join(self.root_dir, format)
        else:
            return format

    def _paths_for_dt_cam(self, time, cam_id=None, abs=False):
        paths = []
        if cam_id is None:
            for cam_id in self.valid_cam_ids:
                paths.append(self._path_for_dt_cam(time, cam_id, abs))
        else:
            paths.append(self._path_for_dt_cam(time, cam_id, abs))
        return paths

    def _all_videos_in(self, path):
        assert type(path) == str

        if not os.path.isdir(path):
            return []
        return [f for f in os.listdir(path) if f.lower().endswith(self.video_ext)]

    def _parse_video_fname(self, fname):
        pass

    def find(self, ts, cam_id=None):
        """Returns all video file paths that belong to the `ts`.

        Args:
            ts (datetime): timestamp to search for.
            cam_id (int): camera id to search for.

        Returns:
            list(string): paths of video files
        """
        # TODO(gitmirgut): Check if 20min is to big and if its also needed for time near 23:59..
        dt = bbb_p.to_datetime(ts)
        paths = self._paths_for_dt_cam(dt, cam_id, abs=True)

        # check if time is near 0 hour, to get paths from the day before.
        time_delta = datetime.timedelta(minutes=20)
        shift_time = dt - time_delta
        if shift_time.day != dt.day:
            paths = paths + self._paths_for_dt_cam(shift_time, cam_id, abs=True)
        video_paths = []
        for path in paths:
            fnames = self._all_videos_in(path)
            fname_parts = [(f, bbb_p.parse_video_fname(f)) for f in fnames]
            for fname, (camId, begin, end) in fname_parts:
                if begin <= dt < end:
                    video_paths.append(os.path.join(path, fname))
        return video_paths
