import os.path

import pytest

import bb_videos_iterator.video_archiv as video_archiv


@pytest.fixture()
def vid_archiv(main_indir):
    archiv_path = os.path.join(main_indir, 'videos_proxy_2016')
    return video_archiv.Video_Achiv(archiv_path)
