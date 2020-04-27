gst-launch-1.0 udpsrc port=5000 ! "application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96" ! rtph264depay ! decodebin ! autovideosink
