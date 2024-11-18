# Build MacOS workstation

## Install Xcode

```bash
xcode-select --install
```

## Package manager

### Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## GIT

```bash
brew install git
```

## Python

```bash
brew install python
```

## Node.js

```bash
brew install node@20
```

## Visual Studio Code

```bash
brew install --cask visual-studio-code
```

## Github CLI

```bash
brew install gh
```

## DBeaver

```bash
brew install --cask dbeaver-community
```

## MongoDB

```bash
brew tap mongodb/brew
brew install mongodb-community
```

## MySQL

```bash
brew install mysql
```

## QEMU

```bash
brew install qemu
```

## reminders-menubar

```bash
brew install --cask reminders-menubar
```

## WGet

```bash
brew install wget
```

## UTM

[Download UTM](https://docs.getutm.app/installation/macos/)

## Step Two

[Step Two - Download](https://apps.apple.com/ca/app/step-two/id1448916662?mt=12)

## Dropbox

[Download Dropbox](https://www.dropbox.com/install)

## Strongbox

[Strongbox - Appstore](https://apps.apple.com/ca/app/strongbox-non-universal/id1270075435?mt=12)

### Strongbox SSH Agent

[Strongbox SSH Agent](https://strongboxsafe.com/support/#reamaze#0#/kb/ssh-agent/ssh-agent)

### Configurer aliases

```bash
brew install sebglazebrook/aliases/aliases
```

Fichier .aliases

```bash
venv:
  command: source venv/bin/activate
gh-deploy:
  command: mkdocs gh-deploy

# Pour accélérer TimeMachine
throttle-off:
  command: sudo sysctl debug.lowpri_throttle_enabled=0
throttle-on:
  command: sudo sysctl debug.lowpri_throttle_enabled=1
# Kill Dock - si command-tab marche plus
killdock:
  command: killall Dock; echo "Command-tab devrait maintenant marcher";
olive:
  command: ssh etienne@olive.profinfo.ca -p 822
olive-local:
  command: ssh etienne@192.168.2.38
start-tunnel:
  command: ssh -f -N -M -S /tmp/sshtunnel -D 1080 etienne@olive.profinfo.ca -p822
stop-tunnel:
  command: ssh -S /tmp/sshtunnel -O exit olive.profinfo.ca -p822
flush-dns:
  command: sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

## Configure terminal

```bash
PROMPT="%1~ # "
PATH="/opt/homebrew/opt/node@20/bin:/Users/etiennerivard/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/etiennerivard/projets/retroaction:${PATH}"

# aliases
eval "$(aliases init --global)"

# Retroaction
alias retroaction='/Users/etiennerivard/projets/retroaction/venv/bin/python3.13 /Users/etiennerivard/projets/retroaction/retroaction.py'
```

## Snagit

[Snagit - Download](https://www.techsmith.com/download/oldversions)

## Postman

[Postman - Download](https://www.postman.com/downloads/)

## Draw.io

[Draw.io - Download](https://github.com/jgraph/drawio-desktop/releases)

## Antidote

Voir sur le serveur olive

## BitDefender

[BitDefender - Download](https://login.bitdefender.com/central/login.html?lang=en_US

## Office 365

[Office 365 - Download](https://office.com)

## Microsoft Teams

[Microsoft Teams - Download](https://www.microsoft.com/en-ca/microsoft-teams/download-app)

## ChatGPT

[ChatGPT - Download](https://openai.com/chatgpt/desktop/)

## Notion

[Notion - Download](https://www.notion.so/desktop)

## Bartender

[Bartender - Download](https://www.macbartender.com/)

## Discord

[Discord - Download](https://discord.com/download)

## The unarchiver

[The unarchiver - Download](https://apps.apple.com/ca/app/the-unarchiver/id425424353?mt=12)

## VLC

[VLC - Download](https://www.videolan.org/vlc/download-macosx.html)

## MySQL Workbench

[MySQL Workbench - Download](https://dev.mysql.com/downloads/workbench/)

## HandBrake

[HandBrake - Download](https://handbrake.fr/)

### Pour faire fonctionner libdvdcss

- Rename /Applications/Handbrake.app as Handbrake-x64.app.
- Right-click Handbrake-x64.app, select "Get Info", then check the box for "Open using Rosetta"
- Right-click /Applications/Utilities/Terminal.app, select "Duplicate", name it Terminal-x64.app
- Right-click Terminal-x64.app, select "Get Info", then check the box for "Open using Rosetta"
- Open Terminal-x64.app
- run 'arch' and make sure it says 'i386', not 'arm64'
  ```bash
  cd /tmp
  curl -OL https://get.videolan.org/libdvdcss/1.4.3/libdvdcss-1.4.3.tar.bz2
  cat libdvdcss-1.4.3.tar.bz2 | bunzip2 | tar x
  cd libdvdcss-1.4.3
  ./configure --prefix=/usr/local
  make
  sudo make install
  ```
- Now open Handbrake-x64.app and your DVDs should decode correctly.

## Chrome

[Chrome - Download](https://www.google.com/chrome/)

## TypeScript

```bash
npm install -g typescript
```
