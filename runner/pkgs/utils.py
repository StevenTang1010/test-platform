#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:utils.py
@time:2021/12/03
@email:tao.xu2008@outlook.com
@description:
"""
import time
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA


def sleep_progressbar(seconds):
    """
    Print a progress bar, total value: seconds
    :param seconds:
    :return:
    """
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker('-=>')), ' ', ETA()]
    pbar = ProgressBar(widgets=widgets, maxval=seconds).start()
    for i in range(seconds):
        pbar.update(1 * i + 1)
        time.sleep(1)
    pbar.finish()


if __name__ == '__main__':
    pass
