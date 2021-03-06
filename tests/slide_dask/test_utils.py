from triad.utils.pyarrow import expression_to_schema
from slide.utils import SlideUtils
from slide_test.suite import SlideTestSuite

from slide_dask.utils import DaskUtils
import pandas as pd
import dask.dataframe as dd
from typing import Any


class DaskTests(SlideTestSuite.Tests):
    def make_utils(self) -> SlideUtils:
        return DaskUtils()

    def to_pd(self, data: Any) -> pd.DataFrame:
        assert isinstance(data, dd.DataFrame)
        return data.compute()

    def to_df(
        self,
        data: Any,
        columns: Any = None,
        coerce: bool = True,
    ):
        if isinstance(columns, str):
            s = expression_to_schema(columns)
            df = dd.from_pandas(
                pd.DataFrame(data, columns=s.names).convert_dtypes(), npartitions=2
            )
            if coerce:
                df = self.utils.cast_df(df, s)
            return df
        elif isinstance(data, list):
            return dd.from_pandas(
                pd.DataFrame(data, columns=columns).convert_dtypes(), npartitions=2
            )
        elif isinstance(data, pd.DataFrame):
            return dd.from_pandas(data.convert_dtypes(), npartitions=2)
        elif isinstance(data, dd.DataFrame):
            return data
        raise NotImplementedError

    def test_cast_int_overflow(self):
        # TODO: Dask doesn't throw when converting inf to int
        pass
