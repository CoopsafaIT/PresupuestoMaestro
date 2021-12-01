MONTH = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

MONTHS_LIST = [
    'Enero',
    'Febrero',
    'Marzo',
    'Abril',
    'Mayo',
    'Junio',
    'Julio',
    'Agosto',
    'Septiembre',
    'Octubre',
    'Noviembre',
    'Diciembre'
]


ZONES = {
    'A': 'Centro America, Belice y Panamá',
    'B': 'Paises del Caribe, Norte y Sur America',
    'C': 'Paises no incluido en las zonas anteriores'
}

TRAVEL_TYPE = {
    1: 'Nacional',
    2: 'Internacional'
}


TRAVEL_CATEGORY = {
    'A': 'A-DIRECTORES',
    'B': 'B-ADMINISTRACIÓN SUPERIOR',
    'C': 'C-EJECUTIVOS Y COMISIONADOS ESPECIALES',
    'D': 'D-MANDOS INTERMEDIOS',
    'E': 'E-PERSONAL ADMINISTRATIVO',
    'F': 'F-PERSONAL DE APOYO TÉCNICO'
}


STAFF_POSITIONS = {
    1: 'Temporal',
    2: 'Permanente'
}


STATUS = (
    ('', '-- Seleccione Estado --'),
    (True, 'Activo'),
    (False, 'Inactivo')
)

STATUS_SCENARIO = (
    ('', '-- Seleccione Estado --'),
    (True, 'Principal'),
    (False, 'Secundario')
)

PROJECTION_TYPES = (
    ('', '-- Seleccione Tipo de Proyección --'),
    ('EXPENSES', 'Gastos'),
    ('INDIRECT', 'Indirecto'),
    ('COSTS', 'Costos'),
    ('INCOME', 'Ingresos'),
)

PROJECTION_SP = (
    ('EXPENSES', '[dbo].[ObtenerEjecutadoDiciembrePresupuestoGastos] '),
    ('INDIRECT', '[dbo].[ObtenerEjecutadoDiciembrePresupuestoIndirecto] '),
    ('COSTS', '[dbo].[ObtenerEjecutadoDiciembrePresupuestoCostos] '),
    ('INCOME', '[dbo].[ObtenerEjecutadoDiciembrePresupuestoIngresos] '),
)

MONTH_CHOICES = (
    ('', '-- Seleccione Mes --'),
    (1, 'Enero'),
    (2, 'Febrero'),
    (3, 'Marzo'),
    (4, 'Abril'),
    (5, 'Mayo'),
    (6, 'Junio'),
    (7, 'Julio'),
    (8, 'Agosto'),
    (9, 'Septiembre'),
    (10, 'Octubre'),
    (11, 'Noviembre'),
    (12, 'Diciembre'),
)

MONTH_CHOICES_REVERSE = (
    ('Enero', 1),
    ('Febrero', 2),
    ('Marzo', 3),
    ('Abril', 4),
    ('Mayo', 5),
    ('Junio', 6),
    ('Julio', 7),
    ('Agosto', 8),
    ('Septiembre', 9),
    ('Octubre', 10),
    ('Noviembre', 11),
    ('Diciembre', 12),
)

LIST_LOAN_PORTFOLIO_FIELDS = [
    {
        'growth_percentage': 'growth_percentage_january',
        'percentage_arrears': 'percentage_arrears_january',
        'commission_percentage': 'commission_percentage_january',
        'rate': 'rate_january',
        'term': 'term_january'
    },
    {
        'growth_percentage': 'growth_percentage_february',
        'percentage_arrears': 'percentage_arrears_february',
        'commission_percentage': 'commission_percentage_february',
        'rate': 'rate_february',
        'term': 'term_february',
    },
    {
        'growth_percentage': 'growth_percentage_march',
        'percentage_arrears': 'percentage_arrears_march',
        'commission_percentage': 'commission_percentage_march',
        'rate': 'rate_march',
        'term': 'term_march',
    },
    {
        'growth_percentage': 'growth_percentage_april',
        'percentage_arrears': 'percentage_arrears_april',
        'commission_percentage': 'commission_percentage_april',
        'rate': 'rate_april',
        'term': 'term_april',
    },
    {
        'growth_percentage': 'growth_percentage_may',
        'percentage_arrears': 'percentage_arrears_may',
        'commission_percentage': 'commission_percentage_may',
        'rate': 'rate_may',
        'term': 'term_may',
    },
    {
        'growth_percentage': 'growth_percentage_june',
        'percentage_arrears': 'percentage_arrears_june',
        'commission_percentage': 'commission_percentage_june',
        'rate': 'rate_june',
        'term': 'term_june',
    },
    {
        'growth_percentage': 'growth_percentage_july',
        'percentage_arrears': 'percentage_arrears_july',
        'commission_percentage': 'commission_percentage_july',
        'rate': 'rate_july',
        'term': 'term_july',
    },
    {
        'growth_percentage': 'growth_percentage_august',
        'percentage_arrears': 'percentage_arrears_august',
        'commission_percentage': 'commission_percentage_august',
        'rate': 'rate_august',
        'term': 'term_august',
    },
    {
        'growth_percentage': 'growth_percentage_september',
        'percentage_arrears': 'percentage_arrears_september',
        'commission_percentage': 'commission_percentage_september',
        'rate': 'rate_september',
        'term': 'term_september',
    },
    {
        'growth_percentage': 'growth_percentage_october',
        'percentage_arrears': 'percentage_arrears_october',
        'commission_percentage': 'commission_percentage_october',
        'rate': 'rate_october',
        'term': 'term_october',
    },
    {
        'growth_percentage': 'growth_percentage_november',
        'percentage_arrears': 'percentage_arrears_november',
        'commission_percentage': 'commission_percentage_november',
        'rate': 'rate_november',
        'term': 'term_november',
    },
    {
        'growth_percentage': 'growth_percentage_december',
        'percentage_arrears': 'percentage_arrears_december',
        'commission_percentage': 'commission_percentage_december',
        'rate': 'rate_december',
        'term': 'term_december',
    },
]


LIST_FINANCIAL_INVESTMENTS_FIELDS = [
    {
        'increases': 'increases_january',
        'decreases': 'decreases_january',
        'rate': 'rate_january',
        'amount_accounts_receivable': 'amount_accounts_receivable_january',
    },
    {
        'increases': 'increases_february',
        'decreases': 'decreases_february',
        'rate': 'rate_february',
        'amount_accounts_receivable': 'amount_accounts_receivable_february',
    },
    {
        'increases': 'increases_march',
        'decreases': 'decreases_march',
        'rate': 'rate_march',
        'amount_accounts_receivable': 'amount_accounts_receivable_march',
    },
    {
        'increases': 'increases_april',
        'decreases': 'decreases_april',
        'rate': 'rate_april',
        'amount_accounts_receivable': 'amount_accounts_receivable_april',
    },
    {
        'increases': 'increases_may',
        'decreases': 'decreases_may',
        'rate': 'rate_may',
        'amount_accounts_receivable': 'amount_accounts_receivable_may',
    },
    {
        'increases': 'increases_june',
        'decreases': 'decreases_june',
        'rate': 'rate_june',
        'amount_accounts_receivable': 'amount_accounts_receivable_june',
    },
    {
        'increases': 'increases_july',
        'decreases': 'decreases_july',
        'rate': 'rate_july',
        'amount_accounts_receivable': 'amount_accounts_receivable_july',
    },
    {
        'increases': 'increases_august',
        'decreases': 'decreases_august',
        'rate': 'rate_august',
        'amount_accounts_receivable': 'amount_accounts_receivable_august',
    },
    {
        'increases': 'increases_september',
        'decreases': 'decreases_september',
        'rate': 'rate_september',
        'amount_accounts_receivable': 'amount_accounts_receivable_september',
    },
    {
        'increases': 'increases_october',
        'decreases': 'decreases_october',
        'rate': 'rate_october',
        'amount_accounts_receivable': 'amount_accounts_receivable_october',
    },
    {
        'increases': 'increases_november',
        'decreases': 'decreases_november',
        'rate': 'rate_november',
        'amount_accounts_receivable': 'amount_accounts_receivable_november',
    },
    {
        'increases': 'increases_december',
        'decreases': 'decreases_december',
        'rate': 'rate_december',
        'amount_accounts_receivable': 'amount_accounts_receivable_december',
    },
]

LIST_SAVINGS_LIABILITIES_FIELDS = [
    {
        'growth_percentage': 'growth_percentage_january',
        'rate': 'rate_january',
    },
    {
        'growth_percentage': 'growth_percentage_february',
        'rate': 'rate_february',
    },
    {
        'growth_percentage': 'growth_percentage_march',
        'rate': 'rate_march',
    },
    {
        'growth_percentage': 'growth_percentage_april',
        'rate': 'rate_april',
    },
    {
        'growth_percentage': 'growth_percentage_may',
        'rate': 'rate_may',
    },
    {
        'growth_percentage': 'growth_percentage_june',
        'rate': 'rate_june',
    },
    {
        'growth_percentage': 'growth_percentage_july',
        'rate': 'rate_july',
    },
    {
        'growth_percentage': 'growth_percentage_august',
        'rate': 'rate_august',
    },
    {
        'growth_percentage': 'growth_percentage_september',
        'rate': 'rate_september',
    },
    {
        'growth_percentage': 'growth_percentage_october',
        'rate': 'rate_october',
    },
    {
        'growth_percentage': 'growth_percentage_november',
        'rate': 'rate_november',
    },
    {
        'growth_percentage': 'growth_percentage_december',
        'rate': 'rate_december',
    },
]

LIST_LIABILITIES_LOANS_FIELDS = [
    {
        'growth_percentage': 'growth_percentage_january',
        'rate': 'rate_january',
        'term': 'term_january',
    },
    {
        'growth_percentage': 'growth_percentage_february',
        'rate': 'rate_february',
        'term': 'term_february',
    },
    {
        'growth_percentage': 'growth_percentage_march',
        'rate': 'rate_march',
        'term': 'term_march',
    },
    {
        'growth_percentage': 'growth_percentage_april',
        'rate': 'rate_april',
        'term': 'term_april',
    },
    {
        'growth_percentage': 'growth_percentage_may',
        'rate': 'rate_may',
        'term': 'term_may',
    },
    {
        'growth_percentage': 'growth_percentage_june',
        'rate': 'rate_june',
        'term': 'term_june',
    },
    {
        'growth_percentage': 'growth_percentage_july',
        'rate': 'rate_july',
        'term': 'term_july',
    },
    {
        'growth_percentage': 'growth_percentage_august',
        'rate': 'rate_august',
        'term': 'term_august',
    },
    {
        'growth_percentage': 'growth_percentage_september',
        'rate': 'rate_september',
        'term': 'term_september',
    },
    {
        'growth_percentage': 'growth_percentage_october',
        'rate': 'rate_october',
        'term': 'term_october',
    },
    {
        'growth_percentage': 'growth_percentage_november',
        'rate': 'rate_november',
        'term': 'term_november',
    },
    {
        'growth_percentage': 'growth_percentage_december',
        'rate': 'rate_december',
        'term': 'term_december',
    },
]


OTHERS_ASSETS_CRITERIA = (
    (1, 'Mismo Valor'),
    (2, 'Porcentaje de Aumento'),
    (3, 'Porcentaje de Disminución'),
    (4, 'Nuevo Valor'),
)
