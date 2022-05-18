#!/usr/bin/env bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}

case "$XDG_SESSION_TYPE" in
  'x11')
    /usr/bin/emacs --daemon &
    #lxsession &
    run nm-applet &
    #run pamac-tray &
    numlockx on &
    #blueman-applet &
    #flameshot &
    #picom --config $HOME/.config/picom/picom.conf &
    picom --config ~/.config/picom/picom-blur.conf --experimental-backends &
    #/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
    dunst &
    #feh --randomize --bg-fill ~/.themes/wallpapers/*
    #starting user applications at boot time
    run volumeicon &
    #run discord &
    #nitrogen --random --set-zoom-fill &
    #run caffeine -a &
    run brave &
    variety --profile /home/jpszc/.config/variety/ &
    #run firefox &
    #run thunar &
    #run dropbox &
    #run insync start &
    #run spotify &
    #run atom &
    #run telegram-desktop &
    ;;
  'wayland')
    /usr/bin/emacs --daemon &
    dunst &
    setbg &
    run vivaldi-stable &
    ;;
esac

