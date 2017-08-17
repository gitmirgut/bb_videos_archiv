import os

import iso8601
import pytest

import bb_videos_iterator.video_archiv as video_archiv


@pytest.fixture
def video_archiv_2016(path_archiv_2016):
    return video_archiv.Video_Archiv(year='2016', root_dir=path_archiv_2016)


@pytest.fixture
def video_archiv_2015(path_archiv_2015):
    return video_archiv.Video_Archiv(year='2015', root_dir=path_archiv_2015)


def test_load_default_config(config):
    dts = video_archiv.Video_Archiv(year='2016')
    assert dts.config is not None
    assert dts.root_dir == config['2016']['ROOT_DIR']
    assert dts.dir_format == config['2016']['DIR_FORMAT']
    assert dts.video_ext == config['2016']['VIDEO_EXT']


def test_load_config(path_archiv_2016, config):
    dts = video_archiv.Video_Archiv(year='2016', root_dir=path_archiv_2016, config=config)
    assert dts.config is not None
    assert dts.root_dir == path_archiv_2016
    assert dts.dir_format == config['2016']['DIR_FORMAT']
    assert dts.video_ext == config['2016']['VIDEO_EXT']


def test_path_for_dt_cam(video_archiv_2015, video_archiv_2016):
    ts = iso8601.parse_date("2016-09-02")
    cam_id = 0
    path_dir = video_archiv_2016._path_for_dt_cam(ts, cam_id, abs=True)
    assert path_dir == "/home/mrpoin/Beesbook/bb_videos_iterator/tests/data/in/" \
                       "videos_proxy_2016/2016-09-02/Cam_0"

    ts = iso8601.parse_date("2015-09-02")
    cam_id = 2
    path_dir = video_archiv_2015._path_for_dt_cam(ts, cam_id, abs=True)
    assert path_dir == "/home/mrpoin/Beesbook/bb_videos_iterator/tests/data/in/videos_proxy_2015/" \
                       "20150902/Cam_2"
    bad_cam_id = 666
    with pytest.raises(ValueError):
        video_archiv_2015._path_for_dt_cam(ts, bad_cam_id)


def test_paths_for_dt_cam(video_archiv_2016):
    ts = iso8601.parse_date("2016-09-02")
    cam_id = 0
    path_dirs = video_archiv_2016._paths_for_dt_cam(ts, cam_id)
    assert path_dirs == ['2016-09-02/Cam_0']
    paths_dirs2 = video_archiv_2016._paths_for_dt_cam(ts)
    assert paths_dirs2 == ['2016-09-02/Cam_0', '2016-09-02/Cam_1',
                           '2016-09-02/Cam_2', '2016-09-02/Cam_3']


def test_all_videos_in(video_archiv_2016, path_archiv_2016):
    path = os.path.join(path_archiv_2016, '2016-08-05', 'Cam_0')
    assert video_archiv_2016._all_videos_in(path) == [
        'Cam_0_2016-08-05T00:10:02.585672Z--2016-08-05T00:15:42.428817Z.mkv',
        'Cam_0_2016-08-05T00:15:42.761835Z--2016-08-05T00:21:22.609116Z.mkv',
        'Cam_0_2016-08-05T00:04:22.402199Z--2016-08-05T00:10:02.251240Z.mkv']

    path = 'badfile/directory'
    assert video_archiv_2016._all_videos_in(path) == []


def test_find_by_ts(video_archiv_2015, video_archiv_2016, path_archiv_2015, path_archiv_2016):
    ts = iso8601.parse_date('2016-08-05T00:06')
    videos = video_archiv_2016.find_by_ts(ts, cam_id=0)
    out = os.path.join(path_archiv_2016, '2016-08-05', 'Cam_0',
                       'Cam_0_2016-08-05T00:04:22.402199Z--2016-08-05T00:10:02.251240Z.mkv')
    assert videos == [out]
    ts = iso8601.parse_date('2016-08-05T00:15')
    videos = video_archiv_2016.find_by_ts(ts)
    assert len(videos) == 4

    # notice that the videos of 2015 are in UTC+02:00
    ts = iso8601.parse_date('2015-08-19T22:00:01')
    videos = video_archiv_2015.find_by_ts(ts, cam_id=2)
    out = os.path.join(path_archiv_2015, '20150819', 'Cam_2',
                       'Cam_2_20150819235309_916748_TO_Cam_2_20150820000822_999973.mkv')
    assert videos == [out]
    videos = video_archiv_2015.find_by_ts(ts)
    assert len(videos) == 4

    ts = iso8601.parse_date('2015-08-20T02:00:01')
    videos = video_archiv_2015.find_by_ts(ts, cam_id=2)
    out = os.path.join(path_archiv_2015, '20150820', 'Cam_2',
                       'Cam_2_20150820034523_186685_TO_Cam_2_20150820040226_280203.mkv')
    assert videos == [out]


def test_day_change(video_archiv_2016, path_archiv_2016):
    ts = iso8601.parse_date('2016-08-05T00:3')
    videos = video_archiv_2016.find_by_ts(ts, cam_id=3)
    out = os.path.join(path_archiv_2016, '2016-08-04', 'Cam_3',
                       'Cam_3_2016-08-04T23:59:39.924786Z--2016-08-05T00:05:19.771866Z.mkv')
    assert videos == [out]


def test_get_abs_path_by_name(video_archiv_2015, video_archiv_2016,
                              path_archiv_2015, path_archiv_2016):
    video = video_archiv_2016.get_abs_path_by_name(
        'Cam_3_2016-08-04T23:59:39.924786Z--2016-08-05T00:05:19.771866Z.mkv')
    out = os.path.join(path_archiv_2016, '2016-08-04', 'Cam_3',
                       'Cam_3_2016-08-04T23:59:39.924786Z--2016-08-05T00:05:19.771866Z.mkv')
    assert video == out

    video = video_archiv_2015.get_abs_path_by_name(
        'Cam_2_20150820034523_186685_TO_Cam_2_20150820040226_280203.mkv')
    out = os.path.join(path_archiv_2015, '20150820', 'Cam_2',
                       'Cam_2_20150820034523_186685_TO_Cam_2_20150820040226_280203.mkv')
    assert video == out

    video = video_archiv_2015.get_abs_path_by_name(
        'Cam_2_20150820034523_186685_TO_Cam_2_20150820040226_23.mk')
    assert video is None


def test_find_closest_videos(video_archiv_2015, video_archiv_2016, path_archiv_2015,
                             path_archiv_2016):
    ts = iso8601.parse_date('2015-09-01T04:06')
    prev, succ = video_archiv_2015.find_closest_videos(ts, 0, abs=False)
    assert prev == "Cam_0_20150901055504_872230_TO_Cam_0_20150901060045_889735.mkv"
    assert succ == "Cam_0_20150901060627_574278_TO_Cam_0_20150901061208_591783.mkv"

    prev, succ = video_archiv_2015.find_closest_videos(ts, 0, abs=True)
    out_dir = os.path.join(path_archiv_2015, '20150901', 'Cam_0')
    assert prev == os.path.join(out_dir,
                                "Cam_0_20150901055504_872230_TO_Cam_0_20150901060045_889735.mkv")
    assert succ == os.path.join(out_dir,
                                "Cam_0_20150901060627_574278_TO_Cam_0_20150901061208_591783.mkv")

    ts = iso8601.parse_date('2015-08-19T22:00:01')
    closest = video_archiv_2015.find_closest_videos(ts, 0, abs=True)
    out_dir = os.path.join(path_archiv_2015, '20150819', 'Cam_0')
    out = os.path.join(out_dir,
                       "Cam_0_20150819234428_462922_TO_Cam_0_20150820000131_555440.mkv")
    assert [out] == closest