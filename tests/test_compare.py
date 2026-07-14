from compare import compare_texts


def test_compare_identical_texts_gives_full_similarity() -> None:
    text = "Hello world, this is a test document."
    result = compare_texts(text, text)
    assert result.similarity_percent == 100.0
    assert result.local_char_count == len(text)
    assert result.azure_char_count == len(text)


def test_compare_completely_different_texts_gives_low_similarity() -> None:
    result = compare_texts("aaaaaaaaaa", "zzzzzzzzzz")
    assert result.similarity_percent == 0.0


def test_compare_similar_texts_gives_partial_similarity() -> None:
    local = "The quick brown fox jumps over the lazy dog."
    azure = "The quick brown fox jumps over the lazy dog!"
    result = compare_texts(local, azure)
    assert 90.0 < result.similarity_percent < 100.0


def test_compare_diff_output_is_a_list_of_strings() -> None:
    result = compare_texts("line one\nline two", "line one\nline three")
    assert isinstance(result.diff, list)
    assert len(result.diff) > 0
