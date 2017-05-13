import os.path

import pytest

import bb_videos_iterator.video_archiv as video_archiv


@pytest.fixture()
def vid_archiv(main_indir):
    archiv_path = os.path.join(main_indir, 'videos_proxy')
    return video_archiv.Video_Achiv(archiv_path)
