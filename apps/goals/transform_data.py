import pandas as pd

# from utils.constants import LOAN_GROWTH, SAVINGS_GROWTH


def calculate_rating(data):
    df = pd.DataFrame(data)
    df['Calificacion'] = df.Ponderacion * df.Porcentaje
    # df_loan_growth = df.loc[df['Nivel1'] == LOAN_GROWTH]
    # first_row_df_loan_growth = df_loan_growth.iloc[:1]
    # df_savings_growth = df.loc[df['Nivel1'] == SAVINGS_GROWTH]
    # df_loan_growth_sum = df_loan_growth.groupby(["Nivel1", ]).sum()
    # df_loan_growth_sum["Nivel2"] = df_loan_growth_sum["Nivel1"]
    total = df.sum()
    total.name = 'Total'
    total_rating = total.Calificacion

    return [df.to_dict(orient='records'), total_rating]
