
def model_predict(model, df):
    """
    Use the trained model to predict using an input dataframe
    :param model: Path of the model
    :param df: Dataframe to be predicted
    :return df_feat: Dataframe with predictions column
    """
    df_feat = df.drop(['status', 'id'], axis=1).dropna()
    df_feat['predictions'] = model.predict(df_feat)
    return df_feat
