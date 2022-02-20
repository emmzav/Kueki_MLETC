import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score, precision_score, roc_auc_score


class ModelTrain:

    def __init__(self, df_feat):
        """
        Constructor
        """
        self.df_feat = df_feat
        self.x = None
        self.y = None
        self.x_balance = None
        self.y_balance = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.model = None

    def data_smote(self):
        """
        Calculate the number of previous loans
        """
        self.y = self.df_feat['status'].astype('int')
        self.df_feat.drop(['status', 'id'], axis=1, inplace=True)
        self.x = self.df_feat
        self.x_balance, self.y_balance = SMOTE().fit_resample(self.x, self.y)

    def data_split(self):
        """
        Calculate the number of previous loans
        """
        self.x_balance = pd.DataFrame(self.x_balance, columns=self.x.columns)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x_balance,  self.y_balance,
                                                                                stratify=self.y_balance, test_size=0.3,
                                                                                random_state=123)

    def random_forest_train(self):
        """
        Calculate the number of previous loans
        """
        self.model = RandomForestClassifier(n_estimators=5)
        self.model.fit(self.x_train, self.y_train)
        return self.model

    def model_metrics(self):
        """
        Calculate the number of previous loans
        """
        y_predict = self.model.predict(self.x_test)
        print(pd.DataFrame(confusion_matrix(self.y_test, y_predict)))
        print('Accuracy Score is {:.5}'.format(accuracy_score(self.y_test, y_predict)))
        print('Precision Score is {:.5}'.format(precision_score(self.y_test, y_predict)))
        print('Recall Score is {:.5}'.format(recall_score(self.y_test, y_predict)))
        print('Roc AUC Score is {:.5}'.format(roc_auc_score(self.y_test, y_predict)))

