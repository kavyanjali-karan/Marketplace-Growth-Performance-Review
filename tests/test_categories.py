def test_categories(df):

    assert df.category.isnull().sum()==0