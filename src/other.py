"This module contains clear "
from src.data_store import data_store

def clear_v1():
    """
    This function exists for the purpose of clearing the data in data_store

    Arguments:
    None

    Exceptions:
    None

    Return Value:
    None
    """
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store["DMs"] = []
    store['tokens'] = []
    store['m_id_create'] = 0
    store['channels_change'] = []
    store['no_channels'] = []
    store['DMs_change'] = []
    store['no_dms'] = []
    store['msg_change'] = []
    store['no_msg'] = []
    store['total_no_msg'] = 0
    store['total_no_chs'] = 0
    store['total_no_dms'] = 0

    data_store.set(store)
