def center(win):  # centers a window
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def sort_column(tv, col, reverse):  # sorts columns of a view tree
    elems = [(tv.set(k, col), k) for k in tv.get_children('')]
    elems.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(elems):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: sort_column(tv, col, not reverse))
