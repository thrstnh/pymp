

def handle_time(time):
        m, s = divmod(time, 60)
        if m < 60:
            return "%02i:%02i" % (m, s)
        else:
            h, m = divmod(m, 60)
            return "%i:%02i:%02i" % (h, m, s)
