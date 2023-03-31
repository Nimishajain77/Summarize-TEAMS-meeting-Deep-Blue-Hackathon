def break_up_file(tokens, chunk_size, overlap_size):
        if len(tokens) <= chunk_size:
            yield tokens
        else:
            chunk = tokens[:chunk_size]
            yield chunk
            yield from break_up_file(
                tokens[chunk_size - overlap_size :], chunk_size, overlap_size
            )