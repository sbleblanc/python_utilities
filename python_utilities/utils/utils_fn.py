def print_progress_bar(current, total, add_text=None):
    percent = (current * 100) // total
    pb = ""
    for _ in range(percent // 20):
        pb += "#"
    if add_text:
        print('\r{:3}%[{:5}] : {}'.format(percent, pb, add_text), end="")
    else:
        print('\r{:3}[{:5}]'.format(percent, pb), end="")
    if percent == 100:
        print()
