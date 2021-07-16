# My QRZ Page

This repo contains the source that generates the dynamic content of [my QRZ page](https://www.qrz.com/db/VA3ZZA).

When a user opens my QRZ page, an Iframe is loaded, which points to this server. The Python scripts in `api/` go out to various data sources, fetch some relevant info about me, then build the result and serve it as a webpage.