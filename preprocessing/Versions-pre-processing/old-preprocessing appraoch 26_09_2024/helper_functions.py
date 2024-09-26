import pickle

def get_all_user_ids(pkl_file_path: str) -> list:
    """
    Load a .pkl file and query for all user IDs.

    Args:
        pkl_file_path (str): The path to the .pkl file.

    Returns:
        list: A list of all user IDs.
    """
    with open(pkl_file_path, 'rb') as f:
        df = pickle.load(f)

    user_ids = df['ID_CommunityIdentity'].tolist()
    return user_ids