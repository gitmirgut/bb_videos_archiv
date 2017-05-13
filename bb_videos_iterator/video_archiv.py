import os

import bb_binary.parsing as bbb_p


class Video_Achiv(object):
    """The Video Archiv class manages multiple video files of the beesbook project."""

    def __init__(self, root_dir):
        """
        Set the root dir of the videos.

        Args:
            root_dir: root directory of the videos.
        """
        self.root_dir = root_dir

    def find(self, ts, cam=None):
        """Return all video paths which match the timestamp `ts`.

        Args:
            ts: timestamp
            cam (int): camera

        Returns:
            Video paths that match the timestamp.
        """

        dt = bbb_p.to_datetime(ts)
        path = self._path_for_dt_cam(dt, cam)
        if not os.path.exists(os.path.join(self.root_dir, path)):
            return []
        print(path)
