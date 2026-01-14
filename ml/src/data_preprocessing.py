"""
Data preprocessing utilities untuk Machine Learning.
Fungsi untuk pembersihan data, handling missing values, dan normalisasi.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from typing import Tuple, List, Optional, Dict
import warnings

warnings.filterwarnings('ignore')


class DataPreprocessor:
    """Class untuk preprocessing data machine learning."""

    def __init__(self):
        """Initialize preprocessor dengan scalers dan encoders."""
        self.scaler = None
        self.label_encoders = {}
        self.imputers = {}
        self.feature_names = []

    def load_data(self, filepath: str, **kwargs) -> pd.DataFrame:
        """
        Load data dari file (CSV, Excel, dll).

        Args:
            filepath: Path ke file data
            **kwargs: Arguments tambahan untuk pandas read function

        Returns:
            DataFrame: Data yang sudah di-load
        """
        try:
            if filepath.endswith('.csv'):
                df = pd.read_csv(filepath, **kwargs)
            elif filepath.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(filepath, **kwargs)
            elif filepath.endswith('.json'):
                df = pd.read_json(filepath, **kwargs)
            else:
                raise ValueError(f"Format file tidak didukung: {filepath}")

            print(f"✓ Data berhasil di-load: {df.shape[0]} rows, {df.shape[1]} columns")
            return df

        except Exception as e:
            print(f"✗ Error loading data: {str(e)}")
            raise

    def check_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Check missing values dalam dataset.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame: Summary missing values
        """
        missing = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': df.isnull().sum().values,
            'Missing_Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
        })

        missing = missing[missing['Missing_Count'] > 0].sort_values(
            'Missing_Percentage',
            ascending=False
        )

        if len(missing) > 0:
            print(f"\n⚠ Found {len(missing)} columns with missing values:")
            print(missing.to_string(index=False))
        else:
            print("\n✓ No missing values found")

        return missing

    def handle_missing_values(
        self,
        df: pd.DataFrame,
        strategy: str = 'auto',
        numerical_strategy: str = 'mean',
        categorical_strategy: str = 'most_frequent'
    ) -> pd.DataFrame:
        """
        Handle missing values dalam dataset.

        Args:
            df: Input DataFrame
            strategy: 'auto', 'drop', atau 'impute'
            numerical_strategy: 'mean', 'median', 'mode', atau 'constant'
            categorical_strategy: 'most_frequent' atau 'constant'

        Returns:
            DataFrame: Data dengan missing values yang sudah di-handle
        """
        df_clean = df.copy()

        if strategy == 'drop':
            # Drop rows dengan missing values
            df_clean = df_clean.dropna()
            print(f"✓ Dropped rows with missing values. New shape: {df_clean.shape}")

        elif strategy in ['impute', 'auto']:
            # Impute numerical columns
            numerical_cols = df_clean.select_dtypes(include=['int64', 'float64']).columns
            if len(numerical_cols) > 0:
                for col in numerical_cols:
                    if df_clean[col].isnull().sum() > 0:
                        if numerical_strategy == 'mean':
                            df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                        elif numerical_strategy == 'median':
                            df_clean[col].fillna(df_clean[col].median(), inplace=True)
                        elif numerical_strategy == 'mode':
                            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)

                print(f"✓ Imputed {len(numerical_cols)} numerical columns using {numerical_strategy}")

            # Impute categorical columns
            categorical_cols = df_clean.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) > 0:
                for col in categorical_cols:
                    if df_clean[col].isnull().sum() > 0:
                        if categorical_strategy == 'most_frequent':
                            df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
                        elif categorical_strategy == 'constant':
                            df_clean[col].fillna('Unknown', inplace=True)

                print(f"✓ Imputed {len(categorical_cols)} categorical columns using {categorical_strategy}")

        return df_clean

    def remove_duplicates(self, df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Remove duplicate rows.

        Args:
            df: Input DataFrame
            subset: Columns to consider for duplicates

        Returns:
            DataFrame: Data tanpa duplikasi
        """
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=subset, keep='first')
        removed_count = initial_count - len(df_clean)

        if removed_count > 0:
            print(f"✓ Removed {removed_count} duplicate rows")
        else:
            print("✓ No duplicates found")

        return df_clean

    def encode_categorical(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'label'
    ) -> pd.DataFrame:
        """
        Encode categorical variables.

        Args:
            df: Input DataFrame
            columns: Columns to encode (None = auto-detect)
            method: 'label' atau 'onehot'

        Returns:
            DataFrame: Data dengan categorical yang sudah di-encode
        """
        df_encoded = df.copy()

        if columns is None:
            columns = df_encoded.select_dtypes(include=['object', 'category']).columns.tolist()

        if method == 'label':
            for col in columns:
                if col in df_encoded.columns:
                    le = LabelEncoder()
                    df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                    self.label_encoders[col] = le

            print(f"✓ Label encoded {len(columns)} categorical columns")

        elif method == 'onehot':
            df_encoded = pd.get_dummies(df_encoded, columns=columns, drop_first=True)
            print(f"✓ One-hot encoded {len(columns)} categorical columns")

        return df_encoded

    def normalize_data(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'standard'
    ) -> pd.DataFrame:
        """
        Normalize/standardize numerical data.

        Args:
            df: Input DataFrame
            columns: Columns to normalize (None = all numerical)
            method: 'standard' (z-score) atau 'minmax' (0-1 scaling)

        Returns:
            DataFrame: Normalized data
        """
        df_normalized = df.copy()

        if columns is None:
            columns = df_normalized.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        else:
            raise ValueError(f"Method tidak valid: {method}")

        df_normalized[columns] = self.scaler.fit_transform(df_normalized[columns])
        print(f"✓ Normalized {len(columns)} columns using {method} scaling")

        return df_normalized

    def remove_outliers(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        method: str = 'iqr',
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        Remove outliers dari dataset.

        Args:
            df: Input DataFrame
            columns: Columns to check (None = all numerical)
            method: 'iqr' atau 'zscore'
            threshold: IQR multiplier (default 1.5) atau z-score threshold (default 3)

        Returns:
            DataFrame: Data tanpa outliers
        """
        df_clean = df.copy()
        initial_count = len(df_clean)

        if columns is None:
            columns = df_clean.select_dtypes(include=['int64', 'float64']).columns.tolist()

        if method == 'iqr':
            for col in columns:
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR

                df_clean = df_clean[
                    (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
                ]

        elif method == 'zscore':
            from scipy import stats
            for col in columns:
                z_scores = np.abs(stats.zscore(df_clean[col]))
                df_clean = df_clean[z_scores < threshold]

        removed_count = initial_count - len(df_clean)
        print(f"✓ Removed {removed_count} outliers using {method} method")

        return df_clean

    def split_features_target(
        self,
        df: pd.DataFrame,
        target_column: str
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Split data menjadi features (X) dan target (y).

        Args:
            df: Input DataFrame
            target_column: Nama kolom target

        Returns:
            Tuple[DataFrame, Series]: X (features) dan y (target)
        """
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        self.feature_names = X.columns.tolist()

        print(f"✓ Split data: X shape {X.shape}, y shape {y.shape}")
        return X, y

    def get_data_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistik dari data.

        Args:
            df: Input DataFrame

        Returns:
            Dict: Summary statistik
        """
        summary = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'numerical_summary': df.describe().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # in MB
        }

        print("\n" + "="*50)
        print("DATA SUMMARY")
        print("="*50)
        print(f"Shape: {summary['shape']}")
        print(f"Memory Usage: {summary['memory_usage']:.2f} MB")
        print(f"\nColumn Types:")
        for dtype, count in df.dtypes.value_counts().items():
            print(f"  {dtype}: {count} columns")

        return summary

    def preprocess_pipeline(
        self,
        df: pd.DataFrame,
        target_column: Optional[str] = None,
        handle_missing: bool = True,
        remove_duplicates: bool = True,
        encode_categorical: bool = True,
        normalize: bool = True,
        remove_outliers: bool = False
    ) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """
        Full preprocessing pipeline.

        Args:
            df: Input DataFrame
            target_column: Target column untuk supervised learning
            handle_missing: Handle missing values
            remove_duplicates: Remove duplicate rows
            encode_categorical: Encode categorical variables
            normalize: Normalize numerical variables
            remove_outliers: Remove outliers

        Returns:
            Tuple: Preprocessed X (dan y jika target_column diberikan)
        """
        print("\n" + "="*50)
        print("STARTING PREPROCESSING PIPELINE")
        print("="*50)

        df_processed = df.copy()

        # 1. Check data info
        self.get_data_summary(df_processed)

        # 2. Check missing values
        self.check_missing_values(df_processed)

        # 3. Handle missing values
        if handle_missing:
            df_processed = self.handle_missing_values(df_processed)

        # 4. Remove duplicates
        if remove_duplicates:
            df_processed = self.remove_duplicates(df_processed)

        # 5. Encode categorical
        if encode_categorical:
            df_processed = self.encode_categorical(df_processed)

        # 6. Remove outliers (before normalization)
        if remove_outliers:
            df_processed = self.remove_outliers(df_processed)

        # 7. Normalize
        if normalize:
            df_processed = self.normalize_data(df_processed)

        # 8. Split features and target
        if target_column:
            X, y = self.split_features_target(df_processed, target_column)
            print("\n" + "="*50)
            print("PREPROCESSING COMPLETE")
            print("="*50)
            return X, y
        else:
            print("\n" + "="*50)
            print("PREPROCESSING COMPLETE")
            print("="*50)
            return df_processed, None
