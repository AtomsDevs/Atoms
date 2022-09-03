import os
import sys
import gettext
import locale


def get_translations():
    '''
    This code snippet searches and load translations from different 
    directories, depending on your production or development environment. 
    '''
    share_dir = os.path.join(sys.prefix, 'share')
    base_dir = '.'

    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        share_dir = os.path.join(base_dir, 'share')
    elif sys.argv[0]:
        exec_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        base_dir = os.path.dirname(exec_dir)
        share_dir = os.path.join(base_dir, 'share')

        if not os.path.exists(share_dir):
            share_dir = base_dir

    locale_dir = os.path.join(share_dir, 'locale')

    if not os.path.exists(locale_dir):  # development
        locale_dir = os.path.join(base_dir, 'build', 'mo')

    locale.bindtextdomain("atoms", locale_dir)
    locale.textdomain("atoms")
    gettext.bindtextdomain("atoms", locale_dir)
    gettext.textdomain("atoms")

    return gettext.gettext
