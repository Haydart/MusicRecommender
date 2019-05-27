def chunk_spotify_track_uri_list(track_uri_list, limit=50):
    for i in range(0, len(track_uri_list), limit):
        yield track_uri_list[i:i + limit]


def list_duplicate_indices(sequence, item):
    return [i for i, x in enumerate(sequence) if x.lower() == item.lower()]
