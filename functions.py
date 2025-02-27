def convert_to_duration(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    duration = ""

    if hours > 0:
        duration = "%02i:%02i:%02i" % (int(hours), int(minutes), int(seconds))
    else:
        duration = "%02i:%02i"  % (int(minutes), int(seconds))

    return duration