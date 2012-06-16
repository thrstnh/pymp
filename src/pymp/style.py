import os
from .logger import init_logger
from .config import init_env

__all__ = ['iconset', 'css_style']
logger = init_logger()
PYMPENV = init_env()


iconsetDefault = {
           "arr_down": 'arr_down.png',
           "arr_left": 'arr_left.png',
           "arr_right": 'arr_right.png',
           "arr_up": 'arr_up.png',
           "cancel": 'cancel.png',
           "clear": 'clear.png',
           "cut": 'cut.png',
           "delete": 'delete.png',
           "error": 'error.png',
           "exit": 'exit.png',
           "filter": 'filter.png',
           "focus": 'focus.png',
           "layout_lm": 'layout_lm.png',
           "layout_lp": 'layout_lp.png',
           "layout_rm": 'layout_rm.png',
           "layout_rp": 'layout_rp.png',
           "lfm_f": 'lfm_f.png',
           "lfm_t": 'lfm_t.png',
           "love_track": 'love_track.png',
           "new": 'new.png',
           "ok": 'ok.png',
           "open": 'open.png',
           "playback_ff": 'playback_ff.png',
           "playback_next": 'playback_next.png',
           "playback_pause": 'playback_pause.png',
           "playback_play": 'playback_play.png',
           "playback_prev": 'playback_prev.png',
           "playback_rew": 'playback_rew.png',
           "playback_stop": 'playback_stop.png',
           "playback_mute": 'speaker.png',
           "pymp": 'pymp.png',
           "random_f": 'random_f.png',
           "random_t": 'random_t.png',
           "refresh": 'refresh.png',
           "repeat_f": 'repeat_f.png',
           "repeat_t": 'repeat_t.png',
           "save": 'save.png',
           "search": 'search.png',
           "settings": 'settings.png',
           "shuffle": 'shuffle.png',
           "speaker": 'speaker.png',
           "warning": 'warning.png',
           "lookandfeel": 'warning.png'}


def _init_icon_set(icons):
    logger.info('init_icon_set')
    ret = {}
    for k, v in icons.items():
        ret[k] = os.path.join(PYMPENV['ICONSET_PATH'], v)
    return ret

iconset = _init_icon_set(iconsetDefault)

css = '''QWidget {
                border: 0px solid black;
                padding: 0px;
                margin: 0px;}
'''
