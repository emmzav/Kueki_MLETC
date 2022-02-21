
def write_predicts(df, output_path):
    """"
    Write the features dataframe
    :param df: Dataframe with feature columns
    :param output_path: Path to write
    """
    df.to_csv(output_path)
    return 0
