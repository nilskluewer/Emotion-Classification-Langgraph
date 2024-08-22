import pandas as pd
import pickle

class DataPreprocessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None

    def process(self):
        self.df = pd.read_csv(self.file_path)
        self._convert_dates()
        self._handle_missing_values()
        self._convert_id_columns()
        self._create_new_features()

    def _convert_dates(self):
        date_columns = ['PostingCreatedAt', 'ArticlePublishingDate', 'UserCreatedAt']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

    def _handle_missing_values(self):
        self.df['PostingHeadline'] = self.df['PostingHeadline'].fillna('No Headline')
        self.df['PostingComment'] = self.df['PostingComment'].fillna('No Comment')
        self.df['UserGender'] = self.df['UserGender'].fillna('Unknown')
        self.df['UserCommunityName'] = self.df['UserCommunityName'].fillna('Unknown')

    def _convert_id_columns(self):
        id_columns = ['ID_Posting', 'ID_Posting_Parent', 'ID_CommunityIdentity', 'ID_Article']
        for col in id_columns:
            self.df[col] = self.df[col].fillna(0).astype(int)

    def _create_new_features(self):
        self.df['CommentLength'] = self.df['PostingComment'].str.len()
        self.df['DaysSinceUserCreation'] = (self.df['PostingCreatedAt'] - self.df['UserCreatedAt']).dt.days
        self.df['IsReply'] = self.df['ID_Posting_Parent'] != 0
        self.df['PostingHour'] = self.df['PostingCreatedAt'].dt.hour
        self.df['PostingDayOfWeek'] = self.df['PostingCreatedAt'].dt.dayofweek

    @classmethod
    def load_preprocessed_data(cls, input_path: str):
        with open(input_path, 'rb') as f:
            df = pickle.load(f)
        preprocessor = cls(None)
        preprocessor.df = df
        print(f"Preprocessed data loaded from {input_path}")
        return preprocessor
