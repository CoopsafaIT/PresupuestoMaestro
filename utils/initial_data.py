FINANCIAL_INVESTMENT = [
    {"name": "Normales", "is_active": True, "identifier": "1"},
    {"name": "FEC", "is_active": True, "identifier": "2"},
]


SAVINGS_LIABILITIES_CATEGORY = [
    {
        "name": "Aportaciones",
        "is_active": True,
        "identifier": "EXEC sp_pptoMaestroAhorrosAportacionesObtenerSaldoHist @ParametroId =", # NOQA
    },
    {
        "name": "Ahorros Retirables",
        "is_active": True,
        "identifier": "EXEC sp_pptoMaestroAhorrosRetirableObtenerSaldoHist @ParametroId =", # NOQA
    },
    {
        "name": "Previcoop",
        "is_active": True,
        "identifier": "EXEC sp_pptoMaestroAhorrosPrevicoopObtenerSaldoHist @ParametroId =", # NOQA
    },
    {
        "name": "Ahorros CDT",
        "is_active": True,
        "identifier": "EXEC sp_pptoMaestroAhorrosCdtObtenerSaldoHist @ParametroId =",
    },
]


LIABILITIES_LOANS_CATEGORY = [
    {"name": "RAP", "is_active": True, "identifier": "1"},
    {"name": "BANHPROVI", "is_active": True, "identifier": "2"},
    {"name": "BCH", "is_active": True, "identifier": "3"},
    {"name": "BCIE", "is_active": True, "identifier": "4"},
]
