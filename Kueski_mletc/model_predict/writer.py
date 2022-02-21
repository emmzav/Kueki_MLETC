
def write_predicts(df, output_path):
    """"
    Write the features dataframe
    :param df: Dataframe with feature columns
    :param output_path: Path to write
    """
    try:
        df.to_csv(output_path)
    except FileNotFoundError:
        raise FileNotFoundError('The predictions could not been written')
    return 0
