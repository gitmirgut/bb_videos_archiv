import os

import iso8601
import pytest

import bb_videos_iterator.structure as structure


@pytest.fixture
def dts_2016(config):
    return structure.Directory_Tree_Structure(root_dir='/home/mrpoin/Beesbook/bb_videos_iterator/'
                                                       'tests/data/in/videos_proxy_2016',
                                              year='2016')


@pytest.fixture
def dts_2015(config):
    return structure.Directory_Tree_Structure(root_dir='/home/mrpoin/Beesbook/bb_videos_iterator/'
                                                       'tests/data/in/videos_proxy_2015',
                                              year='2015')


def test_load_default():
    dts = structure.Directory_Tree_Structure(root_dir='/home/mrpoin/Beesbook/bb_videos_iterator/'
                                                      'tests/data/in/videos_proxy_2016',
                                             year='2016')
    assert dts.config is not None


def test_path_for_dt_cam(dts_2015, dts_2016):
    ts = iso8601.parse_date("2016-09-02")
    cam_id = 0
    path_dir = dts_2016._path_for_dt_cam(ts, cam_id, abs=True)
    assert path_dir == "/home/mrpoin/Beesbook/bb_videos_iterator/tests/data/in/" \
                       "videos_proxy_2016/2016-09-02/Cam_0"

    ts = iso8601.parse_date("2015-09-02")
    cam_id = 2
    path_dir = dts_2015._path_for_dt_cam(ts, cam_id, abs=True)
    assert path_dir == "/home/mrpoin/Beesbook/bb_videos_iterator/tests/data/in/videos_proxy_2015/" \
                       "20150902/Cam_2"
    bad_cam_id = 666
    with pytest.raises(ValueError):
        dts_2015._path_for_dt_cam(ts, bad_cam_id)


def test_paths_for_dt_cam(dts_2016):
    ts = iso8601.parse_date("2016-09-02")
    cam_id = 0
    path_dirs = dts_2016._paths_for_dt_cam(ts, cam_id)
    assert path_dirs == ['2016-09-02/Cam_0']
    paths_dirs2 = dts_2016._paths_for_dt_cam(ts)
    assert paths_dirs2 == ['2016-09-02/Cam_0', '2016-09-02/Cam_1',
                           '2016-09-02/Cam_2', '2016-09-02/Cam_3']


def test_all_videos_in(dts_2016, archiv_2016):
    path = os.path.join(archiv_2016, '2016-08-05', 'Cam_0')
    assert dts_2016._all_videos_in(path) == [
        'Cam_0_2016-08-05T00:10:02.585672Z--2016-08-05T00:15:42.428817Z.mkv',
        'Cam_0_2016-08-05T00:15:42.761835Z--2016-08-05T00:21:22.609116Z.mkv',
        'Cam_0_2016-08-05T00:04:22.402199Z--2016-08-05T00:10:02.251240Z.mkv']


def test_find(dts_2016):
    ts = iso8601.parse_date('2016-08-05T00:06')
    videos = dts_2016.find(ts, cam_id=0)
    assert videos == ['/home/mrpoin/Beesbook/bb_videos_iterator/tests/data/in/videos_proxy_2016/'
                      '2016-08-05/Cam_0/'
                      'Cam_0_2016-08-05T00:04:22.402199Z--2016-08-05T00:10:02.251240Z.mkv']
    ts = iso8601.parse_date('2016-08-05T00:15')
    videos = dts_2016.find(ts)
    assert len(videos) == 4


def test_find2(dts_2015):
    ts = iso8601.parse_date('2015-08-19T22')
    print(ts)
    videos = dts_2015.find(ts, cam_id=2)
    print(videos)


def test_day_change(dts_2016):
    ts = iso8601.parse_date('2016-08-05T00:3')
    videos = dts_2016.find(ts, cam_id=3)
    print(videos)
