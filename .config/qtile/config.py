# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.backend.wayland import InputConfig
from typing import List  # noqa: F401from typing import List  # noqa: F401

wl_input_rules = {
    "*": InputConfig(kb_layout="latam")
}
def log_test(i):
    f = open("/home/jpszc/.config/qtile/qtile_log.txt", "a")
    f.write(str(i) + "\n")
    f.close()

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
#if qtile.core.name == "x11":
#    mtTerm = "alacritty"
#elif qtile.core.name == "wayland":
# myTerm = "alacritty"
myTerm = "kitty"
myBrowser = "brave" # My browser
myEmacs = "emacsclient -c -a 'emacs' "  # emacs keybindings easier to type
myEditor = "emacsclient -c -a 'emacs' "  # Sets emacs as editor
home = os.path.expanduser('~')
dmscripts = home + "/.dmscripts/"

keys = [
         ### The essentials
         Key([mod], "Return",
             # lazy.spawn(myTerm+" -e fish"),
             lazy.spawn(myTerm),
             desc='Launches My Terminal'
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn(home +"/.local/bin/dm-run"),
             desc='Run Launcher'
             ),
         Key([mod], "f",
             lazy.spawn(myTerm + " lfub"),
             desc='lf- File Manager'
             ),
         Key([mod], "b",
             lazy.spawn(myBrowser),
             desc='vivladi'
             ),
         Key([mod], "Tab",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod, "mod1"], "Tab",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
         Key([mod, "shift"], "c",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.reload_config(),
             desc='Restart Qtile config'
             ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         Key([mod, "shift"], "j",
             lazy.layout.shuffle_down(),
             lazy.layout.section_down(),
             desc='Move windows down in current stack'
             ),
         Key([mod, "shift"], "k",
             lazy.layout.shuffle_up(),
             lazy.layout.section_up(),
             desc='Move windows up in current stack'
             ),
         Key([mod], "h",
             lazy.layout.shrink(),
             lazy.layout.decrease_nmaster(),
             desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
             ),
         Key([mod], "l",
             lazy.layout.grow(),
             lazy.layout.increase_nmaster(),
             desc='Expand window (MonadTall), increase number in master pane (Tile)'
             ),
         Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "space",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),
         ### Stack controls
         Key([mod, "control"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
         Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),
             # INCREASE/DECREASE/MUTE VOLUME
         Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
         Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
         Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

         Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
         Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
         Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
         Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    
     #    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
     #    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
     #    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
     #    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),
         # Emacs programs
         KeyChord([mod],"e", [
             Key([], "e",
                 lazy.spawn(myEmacs + "--eval '(dashboard-refresh-buffer)'"),
                 desc='Launch Emacs'
                 ),
             Key([], "b",
                 lazy.spawn(myEmacs + "--eval '(ibuffer)'"),
                 desc='Launch ibuffer inside Emacs'
                 ),
             Key([], "d",
                 lazy.spawn(myEmacs + "--eval '(dired nil)'"),
                 desc='Launch dired inside Emacs'
                 ),
             Key([], "i",
                 lazy.spawn(myEmacs + "--eval '(erc)'"),
                 desc='Launch erc inside Emacs'
                 ),
             Key([], "n",
                 lazy.spawn(myEmacs + "--eval '(elfeed)'"),
                 desc='Launch elfeed inside Emacs'
                 ),
             Key([], "s",
                 lazy.spawn(myEmacs + "--eval '()'"),
                 desc='Launch the eshell inside Emacs'
                 ),
         ]),
         # Dmenu scripts
         KeyChord([mod], "p", [
             Key([], "e",
                 lazy.spawn(dmscripts + "dm-confedit"),
                 desc='Choose a config file to edit'
                 ),
             Key([], "i",
                 lazy.spawn(dmscripts + "dm-maim"),
                 desc='Take screenshots via dmenu'
                 ),
             Key([], "h",
                 lazy.spawn(dmscripts + "dm-hub"),
                 desc='Open dm-hub'
                 ),
             Key([], "k",
                 lazy.spawn(dmscripts + "dm-kill"),
                 desc='Kill processes via dmenu'
                 ),
             Key([], "l",
                 lazy.spawn(dmscripts + "dm-logout"),
                 desc='A logout menu'
                 ),
             Key([], "m",
                 lazy.spawn(dmscripts + "dm-man"),
                 desc='Search manpages in dmenu'
                 ),
             Key([], "r",
                 lazy.spawn(dmscripts + "dm-reddit"),
                 desc='Search reddit via dmenu'
                 ),
             Key([], "s",
                 lazy.spawn(dmscripts + "dm-websearch"),
                 desc='Search various search engines via dmenu'
                 ),
             Key([], "p",
                 lazy.spawn(dmscripts + "dm-rbw"),
                 desc='Retrieve passwords with dmenu'
                 ),
             Key([], "n",
                 lazy.spawn(dmscripts + "dm-network"),
                 desc='Network Manger Script'
                 ),
         ])
]

groups = [Group("DEV", matches=[Match(wm_class=["vscodium"])], layout='max'),
          Group("WWW", matches=[Match(wm_class=["vivaldi-stable","brave-browser"])], layout='max'),
          Group("SYS", layout='max'),
          Group("DOC", layout='max'),
          Group("VBOX", layout='max'),
          Group("CHAT", layout='max'),
          Group("MUS", layout='max'),
          Group("VID", layout='max'),
          # Group("VID", matches=[Match(wm_class=["mpv"])], layout='max'),
          Group("GFX", layout='floating')]
for count,i in enumerate(groups,1):
    count = str(count)
	# mod1 + letter of group = switch to group
    keys.append(
        Key([mod], count, lazy.group[i.name].toscreen())
    )
	# mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, 'shift'], count, lazy.window.togroup(i.name))
    )
# @hook.subscribe.group_window_add
# def new_window(group, window):
    # if group.name == "VID":
        # qtile.current_screen.set_group(group)

layout_theme = {"border_width": 2,
                "margin": 4,
                "border_focus": "51afef",
                # "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    # layout.TreeTab(
    #      font = "Ubuntu",
    #      fontsize = 10,
    #      sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
    #      section_fontsize = 10,
    #      border_width = 2,
    #      bg_color = "1c1f24",
    #      active_bg = "c678dd",
    #      active_fg = "000000",
    #      inactive_bg = "a9a1e1",
    #      inactive_fg = "1c1f24",
    #      padding_left = 0,
    #      padding_x = 0,
    #      padding_y = 5,
    #      section_top = 10,
    #      section_bottom = 20,
    #      level_shift = 8,
    #      vspace = 3,
    #      panel_width = 200
    #      ),
    layout.Floating(**layout_theme)
]

colors = dict(
	# colorBack = "#282c34",
	colorBack = None,
	colorFore = "#bbc2cf",
	color01 = "#1c1f24",
	color02 = "#ff6c6b",
	color03 = "#98be65",
	color04 = "#da8548",
	color05 = "#51afef",
	color06 = "#c678dd",
	color07 = "#5699af",
	color08 = "#202328",
	color09 = "#5b6268",
	color10 = "#da8548",
	color11 = "#4db5bd",
	color12 = "#ecbe7b",
	color13 = "#3071db",
	color14 = "#a9a1e1",
	color15 = "#46d9ff",
	color16 = "#dfdfdf"
)

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    # font="JetBrainsMonoExtraBold Nerd Font",
    font="Ubuntu Bold",
    fontsize = 11,
    background=colors["colorBack"]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
            widget.Sep(linewidth=0,padding=6),
            widget.Image(
                    filename = "~/.config/qtile/icons/qtilelogo.png",
                    iconsize = 8,
                    background = colors["colorBack"],
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn('jgmenu_run')}
            ),
            widget.Sep(linewidth=0,padding=2),
            widget.GroupBox(
                    font = "Ubuntu Bold",
                    fontsize = 9,
                    margin_y = 5,
                    margin_x = 1,
                    padding_y = 0,
                    padding_x = 0,
                    borderwidth = 3,
                    active = colors["color06"],
                    inactive = colors["color05"],
                    rounded = False,
                    highlight_color = colors["color01"],
                    highlight_method = "line",
                    this_current_screen_border = colors["color05"],
                    this_screen_border = colors["color03"],
                    other_current_screen_border = colors["color05"],
                    other_screen_border = colors["color03"],
                    foreground = colors["colorFore"],
                    background = colors["colorBack"]
            ),
            widget.TextBox(
                    text = '|',
                    font = "Ubuntu Mono",
                    background = colors["colorBack"],
                    foreground = '474747',
                    padding = 2,
                    fontsize = 14
            ),
            widget.CurrentLayout(
                    foreground = colors["color02"],
                    background = colors["colorBack"],
                    # fmt='<span rise="4pt">{}</span>',
                    padding = 1
            ),
            widget.TextBox(
                    text = '|',
                    font = "Ubuntu Mono",
                    background = colors["colorBack"],
                    foreground = '474747',
                    padding = 2,
                    fontsize = 14
            ),
            widget.WindowCount(
                    foreground = colors["color02"],
                    background = colors["colorBack"],
                    show_zero = True,
                    # fmt='<span rise="4pt">{}</span>',
                    padding = 2
            ),
            widget.TextBox(
                    text = '|',
                    font = "Ubuntu Mono",
                    background = colors["colorBack"],
                    foreground = '474747',
                    padding = 2,
                    fontsize = 14
            ),
            widget.TaskList(
                    highlight_method = 'border', # or block
                    icon_size=0,
                    # max_title_width=150,
                    rounded=True,
                    padding_x=0,
                    padding_y=0,
                    margin_y=4,
                    fontsize=12,
                    border=colors["colorBack"],
                    foreground=colors["colorFore"],
                    margin=2,
                    txt_floating='🗗',
                    txt_minimized='>_ ',
                    borderwidth = 1,
                    title_width_method = 'uniform',
                    background=colors["colorBack"],
                    #unfocused_border = 'border'
            ),
            widget.TextBox(
                    text = '|',
                    font = "Ubuntu Mono",
                    background = colors["colorBack"],
                    foreground = '474747',
                    padding = 2,
                    fontsize = 14
            ),
            widget.CPU(
                    foreground = colors["color12"],
                    format = '<span font="Font Awesome 6 Free Solid"></span>{load_percent:>6.2f}%'
            ),
            widget.Net(
                    interface = "eno1",
                    format = '<span font="Font Awesome 6 Free Solid"></span>{down}<span font="Font Awesome 6 Free Solid"> </span>{up}',
                    foreground = colors["color02"],
                    background = colors["colorBack"],
                    prefix='M',
                    padding = 5
            ),
            widget.Memory(
                    foreground = colors["color05"],
                    background = colors["colorBack"],
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                    fmt = '<span font="Font Awesome 6 Free Solid"></span>{}',
                    format = '{MemUsed: .0f}{mm}',
                    padding = 5
            ),
            widget.Clock(
                    foreground = colors["color14"],
                    background = colors["colorBack"],
                    # format = "%A, %B %d - %H:%M "
                    format = "%H:%M "
            ),
            # widget.CheckUpdates(
            #          update_interval = 7200,
            #          distro = "Arch_checkupdates",
            #          display_format = "{updates}",
            #          foreground = colors["color04"],
            #          colour_have_updates = colors["color02"],
            #          colour_no_updates = colors["color05"],
            #          mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
            #          padding = 5,
            #          background = colors["colorBack"]
            #          ),
            widget.Systray(
                    background=colors["colorBack"],
                    icon_size=20,
                    padding = 4
                ),
        ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    # del widgets_screen1[9:10]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

# def init_widgets_screen2():
#   widgets_screen2 = init_widgets_list()
#   return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=24, background="#282c34ff"))]
#   return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
#           Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
#           Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
#   widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),    Match(title='Confirmation'),      # tastyworks exit box
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
