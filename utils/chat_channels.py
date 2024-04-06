def load_channels():
    global CHAT_CHANNELS
    with open("channels.txt", "r") as f:
        CHAT_CHANNELS = [line.strip() for line in f.readlines()]
    return CHAT_CHANNELS

def add_channel(channel):
    global CHAT_CHANNELS
    CHAT_CHANNELS.append(channel)
    with open("channels.txt", "a") as f:
        f.write(channel + "\n")
    return CHAT_CHANNELS

def remove_channel(channel):
    global CHAT_CHANNELS
    CHAT_CHANNELS.remove(channel)
    with open("channels.txt", "w") as f:
        for channel in CHAT_CHANNELS:
            f.write(channel + "\n")
    return CHAT_CHANNELS

def get_channels():
    global CHAT_CHANNELS
    return CHAT_CHANNELS

CHAT_CHANNELS = load_channels()