from src.preprocessing import build_preprocessor, load_raw_dataset, prepare_dataset


def test_load_raw_dataset_has_expected_shape():
    dataframe = load_raw_dataset()
    assert dataframe.shape == (303, 14)


def test_prepare_dataset_binarizes_target():
    dataframe = prepare_dataset(save_processed=False)
    assert set(dataframe["target"].unique()) == {0, 1}


def test_build_preprocessor_returns_transformer():
    preprocessor = build_preprocessor()
    assert hasattr(preprocessor, "fit")
