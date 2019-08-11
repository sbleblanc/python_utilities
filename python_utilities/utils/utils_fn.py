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


def print_kv_box(title: str, key_values, width=80, padding=1):
    print('*' * width)
    usuable_width = width - 2 - padding * 2

    # Print the title
    format_string = '*{{:{}}}{{:^{}}}{{:{}}}*'.format(padding, usuable_width, padding)
    print(format_string.format('', title.upper(), ''))

    # Print the key-value pairs
    format_string = '*{{:{}}}{{:{}}}{{:{}}}*'.format(padding, usuable_width, padding)
    longest = 0
    for k, _ in key_values:
        if len(k) > longest:
            longest = len(k)
    inner_fs = '{{:{}}}: {{}}'.format(longest)
    for k, v in key_values:
        print(format_string.format('', inner_fs.format(k, v), ''))

    print('*' * width)
