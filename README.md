# MightyOmegaBot
- The Mighty Omega Bot
- Silly little discord bot that is used in servers
  - [Всемогущий куб](https://discord.gg/fYmvvGG28C)
  - [Almighty Cube](https://discord.gg/W3DRNP3Wq6)
- Functionality:
  - Some QoL functions (ex. better timeouts, remindme)
  - Silly functions (ex. `/morning_tea`)
  - Basic LaTeX rendering (using `/latex`)
  - Standard functions like `/ping`


# Dependencies
In addition to the dependencies in requirements.txt, this bot (cog LaTeX_Converter) depends on the [TexLive](https://www.tug.org/texlive/) program.


# How to make it work
Add your bot token as the first argument. Ex. "python3 main.py [token here]"


# Docker
- Build image using `sudo docker build -t omegabot .`
- Add secret with your discord token using `sudo docker secret create omegabot-token /path/to/token.txt`
- Create it as a service. Ex. `sudo docker service create --name omegabot-service --secret omegabot-token omegabot`
