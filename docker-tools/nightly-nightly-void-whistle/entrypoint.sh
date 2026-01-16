#!/bin/sh

SOUND_TYPE=${1:-rift}

if [ ! -f "/sounds/$SOUND_TYPE.wav" ]; then
  echo "Unknown sound type: $SOUND_TYPE"
  exit 1
fi

echo "Playing sound: $SOUND_TYPE"
play -q "/sounds/$SOUND_TYPE.wav"
