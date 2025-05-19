# GithubPlaysPokemon

This is a small project that lets you play Pokemon (or any Game Boy or Game Boy Color game) from your Github page!
<br />
<br />
The emulator is hosted server-side so anyone looking at your Github profile will be able to play on the same game and cooperate together (or not, who knows 😈) to reach the end.
<br />
<br />
Supports save through savestates which happens once every 10 minutes and when shutting down the server, and reload the state at boot.

## Installation

### Clone
- Clone the project on your server

### Environnement setup
- Make a copy of `.env.sample` and rename it to `.env`
- Edit this `.env` file to change the running port if needed
- Make a copy of `api/.env.sample` and rename it to `api/.env`
- Edit this `.env` file if you want to change language, rate limits and to enable re-redirection to your Github profile
- Make a copy of `pyboy/.env.sample` and rename it to `pyboy/.env`
- Edit this `.env` file if you want to change the default screenshot delay

### Game setup
- Place a <u><b>legally dumped</b></u> ROM from a game you <u><b>own</b></u> in the `pyboy/rom/` folder and rename it to `game.gb` (Game Boy game) or `game.gbc` (Game Boy Color game)
<br />
*Note: if there's 2 ROM files in the folder, `game.gbc` takes priority over `game.gb`*

### Build
- Build the project with the command:
<br />
```console
$ cd GithubPlaysPokemon/
$ docker compose up --build
```
- Once built, the container will start automatically


### Reverse proxy
- Set up a reverse proxy on `http://localhost:5000` (or the port defined in `.env`) using your prefered web server (Apache, Nginx, ...)

## Usage

### Start the container

Once build for the first time, you can quicky start the container by using this command in the `GithubPlaysPokemon` folder:
```console
$ docker compose up
```

### Stop the container

You can stop the container by using this command in the `GithubPlaysPokemon` folder:
```console
$ docker compose down
```
*Note: If the pyboy container gets shut abruptly, you may end up with a corrupted savestate. When restarting your container, always check that the emulator loads its state correctly, otherwise you may want to replace the state with one of the backups*

### Making your README in your profile

You will find a README template I've made myself in the `resources` folder, you just need to edit the domain name to match yours and it will be ready to use.
<br />
<br />
If you want to make your own README file, you will need to include these links:
### Screen
- `https://your.domain.com/screen/screen.png` : the current screenshot, updated every few seconds on the server but every minutes on GitHub due to its internal cache system
### Inputs
- `https://your.domain.com/input/a` : A button
- `https://your.domain.com/input/b` : B button
- `https://your.domain.com/input/up` : Up arrow
- `https://your.domain.com/input/down` : Down arrow
- `https://your.domain.com/input/left` : Left arrow
- `https://your.domain.com/input/right` : Right arrow
- `https://your.domain.com/input/start` : START button
- `https://your.domain.com/input/select` : SELECT button
