from typing import List

def decompress_nn_output(from_square, to_square):
    """
    Decompresses the output of a neural network.

    Args:
        from_square (float): The compressed 'from' square output from the neural network (normalized 0-1).
        to_square (float): The compressed 'to' square output from the neural network (normalized 0-1).

    Returns:
        tuple[tuple[int, int], tuple[int, int]]: The decompressed output as two (row, col) tuples.
    """
    return (
        square_index_to_coords(min(max(round(from_square * 63), 0), 63)),
        square_index_to_coords(min(max(round(to_square * 63), 0), 63))
    )

def square_index_to_coords(index: int) -> tuple[int, int]:
    """
    Converts 0-63 index to (row, col) where row, col in 0-7.
    Row 0 = rank 1 (bottom), Col 0 = file a (left).
    """
    return divmod(index, 8)  # returns (row, col)