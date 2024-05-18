FROM archlinux:latest
WORKDIR /app
COPY . .
RUN pacman --noconfirm -Syu \
    && pacman --noconfirm -S texlive-basic texlive-latex texlive-latexextra python python-pip \
    && rm -rf /var/cache/pacman/ \
    && pip install --break-system-packages --no-cache-dir -r requirements.txt
CMD python3 main.py $(cat /run/secrets/omegabot-token)
