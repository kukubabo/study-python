#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 [URL]"
  exit 1
fi

yt-dlp -i -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best --yes-playlist $1
