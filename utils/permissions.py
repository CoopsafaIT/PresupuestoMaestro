data_content_types = [
    {"app_label": "ppto_gastos", "model": "ppto_gastos"},
    {"app_label": "ppto_viaticos", "model": "ppto_viaticos"},
    {"app_label": "ppto_indirecto", "model": "ppto_indirecto"},
    {"app_label": "ppto_costos", "model": "ppto_costos"},
    {"app_label": "ppto_personal", "model": "ppto_personal"},
    {"app_label": "ppto_inversion", "model": "ppto_inversion"},
    {"app_label": "ppto_ingresos", "model": "ppto_ingresos"},
    {"app_label": "ppto_maestro", "model": "ppto_maestro"},
    {"app_label": "admin", "model": "admin"},
    {"app_label": "security", "model": "security"},
]

admin_permissions = [

    {
        "name": "Puede Ingresar Proyección",
        "content_type_name": "admin",
        "codename": "puede_ingresar_proyeccion",
    },
    {
        "name": "Puede Listar Proyectos",
        "content_type_name": "admin",
        "codename": "puede_listar_proyectos",
    },
    {
        "name": "Puede Ingresar Periodos",
        "content_type_name": "admin",
        "codename": "puede_ingresar_periodos",
    },
    {
        "name": "Puede Editar Periodos",
        "content_type_name": "admin",
        "codename": "puede_editar_periodos",
    },
    {
        "name": "Puede Listar Periodos",
        "content_type_name": "admin",
        "codename": "puede_listar_periodos",
    },

    {
        "name": "Puede Listar Centros Costos",
        "content_type_name": "admin",
        "codename": "puede_listar_centros_costos",
    },
    {
        "name": "Puede Listar Control Presupuesto Centros Costos",
        "content_type_name": "admin",
        "codename": "puede_listar_control_ppto_centros_costos",
    },
    {
        "name": "Puede Editar Indice Inflacionario",
        "content_type_name": "admin",
        "codename": "puede_editar_indice_inflacionario",
    },
    {
        "name": "Puede Listar Puestos de Trabajo",
        "content_type_name": "admin",
        "codename": "puede_listar_puestos_trabajo",
    },
    {
        "name": "Puede Crear Puestos de Trabajo",
        "content_type_name": "admin",
        "codename": "puede_crear_puestos_trabajo",
    },
    {
        "name": "Puede Editar Puestos de Trabajo",
        "content_type_name": "admin",
        "codename": "puede_editar_puestos_trabajo",
    },
]

security_permissions = [
    {
        "name": "Puede Asignar Usuarios a CECOs",
        "content_type_name": "security",
        "codename": "puede_asignar_usuarios_ceco",
    },
    {
        "name": "Puede Ingresar Usuarios",
        "content_type_name": "security",
        "codename": "puede_ingresar_usuarios",
    },
    {
        "name": "Puede Editar Usuarios",
        "content_type_name": "security",
        "codename": "puede_editar_usuarios",
    },
    {
        "name": "Puede Listar Usuarios",
        "content_type_name": "security",
        "codename": "puede_listar_usuarios",
    },
    {
        "name": "Puede Ingresar Roles",
        "content_type_name": "security",
        "codename": "puede_ingresar_roles",
    },
    {
        "name": "Puede Editar Roles",
        "content_type_name": "security",
        "codename": "puede_editar_roles",
    },
    {
        "name": "Puede Listar Roles",
        "content_type_name": "security",
        "codename": "puede_listar_roles",
    },
]

investment_permissions = [
    {
        "name": "Puede Ingresar Inversiones",
        "content_type_name": "admin",
        "codename": "puede_ingresar_inversiones",
    },
    {
        "name": "Puede Editar Inversiones",
        "content_type_name": "admin",
        "codename": "puede_editar_inversiones",
    },
    {
        "name": "Puede Listar Inversiones",
        "content_type_name": "admin",
        "codename": "puede_listar_inversiones",
    },
    {
        "name": "Puede Ingresar Cuentas Inversion",
        "content_type_name": "admin",
        "codename": "puede_ingresar_cuentas_inversion",
    },
    {
        "name": "Puede Editar Cuentas Inversion",
        "content_type_name": "admin",
        "codename": "puede_editar_cuentas_inversion",
    },
    {
        "name": "Puede Listar Cuentas Inversion",
        "content_type_name": "admin",
        "codename": "puede_listar_cuentas_inversion",
    },
]

travel_budget_permissions = [
    {
        "name": "Puede Distribuir viaticos",
        "content_type_name": "ppto_viaticos",
        "codename": "puede_distribuir_ppto_viaticos",
    },
    {
        "name": "Puede Ingresar PPTO. Viaticos Todos CECO",
        "content_type_name": "ppto_viaticos",
        "codename": "puede_ingresar_ppto_viaticos_todos",
    },
    {
        "name": "Puede Ingresar PPTO. Viaticos CECO Asignados",
        "content_type_name": "ppto_viaticos",
        "codename": "puede_ingresar_ppto_viaticos",
    },
]

expenses_budget_permissions = [
    {
        "name": "Puede Ingresar PPTO. Gastos Todos CECO",
        "content_type_name": "ppto_gastos",
        "codename": "puede_ingresar_ppto_gastos_todos",
    },
    {
        "name": "Puede Ingresar PPTO. Gastos CECO Asignados",
        "content_type_name": "ppto_gastos",
        "codename": "puede_ingresar_ppto_gastos",
    },
]

indirect_budget_permissions = [
    {
        "name": "Puede Ingresar PPTO. Indirecto",
        "content_type_name": "ppto_indirecto",
        "codename": "puede_ingresar_ppto_indirecto",
    },
]

costs_budget_permissions = [
    {
        "name": "Puede Ingresar PPTO. Costos",
        "content_type_name": "ppto_costos",
        "codename": "puede_ingresar_ppto_costos",
    },
]

staff_budget_permissions = [
    {
        "name": "Puede Ingresar PPTO. Personal Todos CECO",
        "content_type_name": "ppto_personal",
        "codename": "puede_ingresar_ppto_personal_todos",
    },
    {
        "name": "Puede Ingresar PPTO. Personal Asignados",
        "content_type_name": "ppto_personal",
        "codename": "puede_ingresar_ppto_personal",
    },
]

income_budget_permissions = [
    {
        "name": "Puede Ingresar PPTO. Ingresos",
        "content_type_name": "ppto_ingresos",
        "codename": "puede_ingresar_ppto_ingresos",
    },
]

investment_budget_permissions = [
    {
        "name": "Puede Ingresar PPTO. Inversion Todos CECO",
        "content_type_name": "ppto_inversion",
        "codename": "puede_ingresar_ppto_inversion_todos",
    },
    {
        "name": "Puede Ingresar PPTO. Inversion Asignados",
        "content_type_name": "ppto_inversion",
        "codename": "puede_ingresar_ppto_inversion",
    },
]

transfers_permissions = [
    {
        "name": "Puede Crear Traslados de Inversion",
        "content_type_name": "ppto_inversion",
        "codename": "puede_crear_traslados_inversion",
    },
    {
        "name": "Puede Crear Traslados de Gastos",
        "content_type_name": "ppto_gastos",
        "codename": "puede_crear_traslados_gastos",
    },
]

checkout_permissions = [
    {
        "name": "Puede Registrar Egresos de Inversion",
        "content_type_name": "ppto_inversion",
        "codename": "puede_registrar_egresos_inversion",
    },
    {
        "name": "Puede Registrar Egresos de Personal",
        "content_type_name": "ppto_personal",
        "codename": "puede_registrar_egresos_personal",
    },
    {
        "name": "Puede Registrar Egresos de Viaticos",
        "content_type_name": "ppto_viaticos",
        "codename": "puede_registrar_egresos_viaticos",
    },
]

all_permissions = (
    admin_permissions
    + security_permissions
    + investment_permissions
    + travel_budget_permissions
    + expenses_budget_permissions
    + indirect_budget_permissions
    + costs_budget_permissions
    + staff_budget_permissions
    + staff_budget_permissions
    + income_budget_permissions
    + investment_budget_permissions
    + transfers_permissions
    + checkout_permissions
)
