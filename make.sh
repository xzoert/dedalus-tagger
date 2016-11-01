#!/bin/bash
pyside-uic tagger.ui -o tagger_widget.py
pyside-rcc -py3 -o tagger_rc.py tagger.qrc

