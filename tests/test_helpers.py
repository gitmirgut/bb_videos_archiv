import bb_videos_iterator.helpers as helpers


def test_get_default_config():
    config = helpers.get_default_config()
    print(config.sections())
    config_set = {
        '2015',
        '2016'}
    assert set(config.sections()) == config_set
