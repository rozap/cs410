#!/bin/sh
while inotifywait -e modify less; do
  lessc less/bootstrap.less > css/style.css
done
