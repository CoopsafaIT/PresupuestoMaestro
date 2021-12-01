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

NON_PERFORMING_ASSETS_CATEGORY = [
    {"name": "TERRENOS", "is_active": True, "identifier": "1"},
    {"name": "EDIFICIOS", "is_active": True, "identifier": "2"},
    {"name": "INSTALACIONES", "is_active": True, "identifier": "3"},
    {"name": "MUEB. Y EQ.", "is_active": True, "identifier": "4"},
    {"name": "VEHICULOS", "is_active": True, "identifier": "5"},
    {"name": "SOFTWARE", "is_active": True, "identifier": "6"},
]

NON_PERFORMING_ASSETS_CATEGORY_PER_ACCOUNTS = [
    {"account_id": "19529", "category_identifier": "2"},
    {"account_id": "18931", "category_identifier": "3"},
    {"account_id": "833", "category_identifier": "3"},
    {"account_id": "18934", "category_identifier": "4"},
    {"account_id": "18932", "category_identifier": "4"},
    {"account_id": "18933", "category_identifier": "4"},
    {"account_id": "835", "category_identifier": "4"},
    {"account_id": "18935", "category_identifier": "4"},
    {"account_id": "834", "category_identifier": "5"},
    {"account_id": "19539", "category_identifier": "6"}
]


OTHERS_ASSETS_CATEGORY = [
    {
        "name": "Otros Activos",
        "is_active": True,
        "identifier": "EXEC [dbo].[sp_pptoMaestroBienesCapitalActivosOtrosActivosObtenerSaldoHist] @ParametroId = " # NOQA
    },
    {
        "name": "Activos Eventuales",
        "is_active": True,
        "identifier": "EXEC [dbo].[sp_pptoMaestroBienesCapitalActivosEventualesObtenerSaldoHist] @ParametroId = " # NOQA
    },
    {
        "name": "Cargos Diferidos",
        "is_active": True,
        "identifier": "EXEC [dbo].[sp_pptoMaestroBienesCapitalActivosCargosDiferidosObtenerSaldoHist] @ParametroId = " # NOQA
    },
    {
        "name": "Activos Monetarios",
        "is_active": True,
        "identifier": "EXEC [dbo].[sp_pptoMaestroBienesCapitalActivosMonetariosObtenerSaldoHist] @ParametroId = " # NOQA
    },
]
