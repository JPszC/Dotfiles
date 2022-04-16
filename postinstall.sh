#!/bin/sh

sudo pacman --noconfirm -Syu
echo "###########################"
echo "## Downloading pkgs.txt. ##"
echo "###########################"
sudo sed -i 's/^#ParallelDownloads/ParallelDownloads/' /etc/pacman.conf
sudo pacman --needed --ask 4 -Sy -< pkgs.txt

echo "#####################################"
echo "## Installing Shell-Color-Scripts. ##"
echo "#####################################"
curl https://gitlab.com/JPszC/shell-color-scripts/-/raw/master/PKGBUILD > PKGBUILD
makepkg -cf
sudo pacman --noconfirm -U shell-color*.pkg.tar.zst
rm -rf shell-color-script* PKGBUILD

echo "#######################"
echo "## Installing dmenu. ##"
echo "#######################"
curl https://gitlab.com/JPszC/dmenu/-/raw/master/PKGBUILD > PKGBUILD
makepkg -cf
sudo pacman --noconfirm -U dmenu*.pkg.tar.zst
rm -rf dmenu* PKGBUILD

echo "#########################################################"
echo "## Installing Doom Emacs. This may take a few minutes. ##"
echo "#########################################################"
git clone --depth 1 https://github.com/hlissner/doom-emacs ~/.emacs.d
~/.emacs.d/bin/doom env
~/.emacs.d/bin/doom -y install
~/.emacs.d/bin/doom sync
