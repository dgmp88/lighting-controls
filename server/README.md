# lighting-controls

## Notes on putting it together:

1. I needed to use grounds _both_ from the pi _and_ from the 12 V power supply. Not sure why.
2. I followed [this tutorial](http://www.modmypi.com/blog/tutorial-how-to-give-your-raspberry-pi-a-static-ip-address) to get a static IP on the pi.
3. I followed [this tutorial](http://twistedmatrix.com/documents/13.2.0/core/howto/systemd.html) to get systemd to start a dameon to run the server on boot.

Copy this to here: 
```sudo cp lightingcontrols.service /etc/systemd/system/```

Start it with 
```sudo systemctl start lightingcontrols.service```

