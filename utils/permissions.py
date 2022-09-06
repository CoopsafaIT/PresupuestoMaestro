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
    {"app_label": "goals", "model": "goals"},
]

admin_permissions = [

    {
        "name": "Puede Ingresar Proyección",
        "content_type_name": "admin",
        "codename": "puede_ingresar_proyeccion",
    },
    {
        "name": "Puede Inicializar Presupuestos",
        "content_type_name": "admin",
        "codename": "puede_inicializar_ppto",
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
    {
        "name": "Puede Ver reportes PPTO. Gastos CECO Asignados",
        "content_type_name": "ppto_gastos",
        "codename": "puede_ver_ppto_gastos",
    },
    {
        "name": "Puede Ver reportes PPTO. Gastos Todos CECO ",
        "content_type_name": "ppto_gastos",
        "codename": "puede_ver_ppto_gastos_todos",
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

master_budget = [
    {
        "name": "Puede Menu de Presupuesto Maestro",
        "content_type_name": "ppto_maestro",
        "codename": "puede_ver_menu_ppto_maestro",
    },
    # Cartera Crediticia
    {
        "name": "Puede Listar Cartera Crediticia",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_cartera_crediticia",
    },
    {
        "name": "Puede Crear Escenarios Cartera Crediticia",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_cartera_crediticia",
    },
    {
        "name": "Puede Editar Escenarios Cartera Crediticia",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_cartera_crediticia",
    },
    # Inversiones Financieras
    {
        "name": "Puede Listar Escenarios Inversiones Financieras",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_inversiones_financieras",
    },
    {
        "name": "Puede Crear Escenarios Inversiones Financieras",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_inversiones_financieras",
    },
    {
        "name": "Puede Editar Escenarios Inversiones Financieras",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_inversiones_financieras",
    },
    # Nuevas Adquisiciones
    {
        "name": "Puede Listar Escenarios Nuevas Adquisiciones",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_nuevas_adquisiciones",
    },
    {
        "name": "Puede Crear Escenarios Nuevas Adquisiciones",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_nuevas_adquisiciones",
    },
    {
        "name": "Puede Editar Escenarios Nuevas Adquisiciones",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_nuevas_adquisiciones",
    },
    # Otros Activos
    {
        "name": "Puede Listar Escenarios Otros Activos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_escenarios_otros_activos",
    },
    {
        "name": "Puede Crear Escenarios Otros Activos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_otros_activos",
    },
    {
        "name": "Puede Editar Escenarios Otros Activos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_otros_activos",
    },
    # Pasivos Ahorros
    {
        "name": "Puede Listar Escenarios Pasivos Ahorros",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_escenarios_pasivos_ahorros",
    },
    {
        "name": "Puede Crear Escenarios Pasivos Ahorros",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_pasivos_ahorros",
    },
    {
        "name": "Puede Editar Escenarios Pasivos Ahorros",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_pasivos_ahorros",
    },
    # Pasivos Prestamos
    {
        "name": "Puede Listar Escenarios Pasivos Prestamos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_escenarios_pasivos_prestamos",
    },
    {
        "name": "Puede Crear Escenarios Pasivos Prestamos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_pasivos_prestamos",
    },
    {
        "name": "Puede Editar Escenarios Pasivos Prestamos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_pasivos_prestamos",
    },
    # Otros Pasivos
    {
        "name": "Puede Listar Escenarios Otros Pasivos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_escenarios_otros_pasivos",
    },
    {
        "name": "Puede Crear Escenarios Otros Pasivos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_otros_pasivos",
    },
    {
        "name": "Puede Editar Escenarios Otros Pasivos",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_otros_pasivos",
    },
    # Patrimonio
    {
        "name": "Puede Listar Escenarios Patrimonio",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_escenarios_patrimonio",
    },
    {
        "name": "Puede Crear Escenarios Patrimonio",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_patrimonio",
    },
    {
        "name": "Puede Editar Escenarios Patrimonio",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_patrimonio",
    },
    # Distribucion de Excedentes
    {
        "name": "Puede Listar Distribucion de Excedentes",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_escenarios_distribucion_excedentes",
    },
    {
        "name": "Puede Crear Distribucion de Excedentes",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_distribucion_excedentes",
    },
    {
        "name": "Puede Editar Distribucion de Excedentes",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_distribucion_excedentes",
    },
    # Planilla
    {
        "name": "Puede Listar Escenarios Planilla",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_escenarios_planilla",
    },
    {
        "name": "Puede Crear Escenarios Planilla",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_escenarios_planilla",
    },
    {
        "name": "Puede Editar Escenarios Planilla",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_escenarios_planilla",
    },

    # Proyeccion complementaria P&G
    {
        "name": "Puede Listar Proyeccion Complementaria P&G",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_proyecccion_complementaria_p_g",
    },
    {
        "name": "Puede Editar Proyeccion Complementaria Ganancias",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_proyecccion_complementaria_ganancias",
    },
    {
        "name": "Puede Editar Proyeccion Complementaria Perdidas",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_proyecccion_complementaria_perdidas",
    },
    # Parametros de Proyeccion
    {
        "name": "Puede Listar Parametros de Proyeccion",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_parametros_proyeccion",
    },
    {
        "name": "Puede Crear Parametros de Proyeccion",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_parametros_proyeccion",
    },
    {
        "name": "Puede Editar Parametros de Proyeccion",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_parametros_proyeccion",
    },

    # Categorias de Prestamos Cartera Crediticia
    {
        "name": "Puede Listar Categorias de Prestamos Cartera Crediticia",
        "content_type_name": "ppto_maestro",
        "codename": "puede_listar_categorias_prestamos",
    },
    {
        "name": "Puede Crear Categorias de Prestamos Cartera Crediticia",
        "content_type_name": "ppto_maestro",
        "codename": "puede_crear_categorias_prestamos",
    },
    {
        "name": "Puede Editar Categorias de Prestamos Cartera Crediticia",
        "content_type_name": "ppto_maestro",
        "codename": "puede_editar_categorias_prestamos",
    },

]

goals_permissions = [
    {
        "name": "Puede Ver Menu de Metas",
        "content_type_name": "goals",
        "codename": "puede_ver_menu_de_metas",
    },
    {
        "name": "Puede Listar Periodos de Metas",
        "content_type_name": "goals",
        "codename": "puede_listar_definicion_de_periodo_de_meta",
    },
    {
        "name": "Puede Ingresar Periodo de Meta",
        "content_type_name": "goals",
        "codename": "puede_ingresar_periodo_de_meta",
    },
    {
        "name": "Puede Editar Periodo de Meta",
        "content_type_name": "goals",
        "codename": "puede_editar_periodo_de_meta",
    },
    {
        "name": "Puede Ver Definicion de Meta",
        "content_type_name": "goals",
        "codename": "puede_ver_definicion_de_meta",
    },

    {
        "name": "Puede Ver Definicion de Meta Asignada",
        "content_type_name": "goals",
        "codename": "puede_ver_definicion_de_meta_asignada",
    },

    {
        "name": "Puede Registrar Metas Globales",
        "content_type_name": "goals",
        "codename": "puede_registrar_metas_globales",
    },
    {
        "name": "Puede Ver Detalle Mensual de Metas Globales",
        "content_type_name": "goals",
        "codename": "puede_ver_detalle_mensual_de_metas_globales",
    },
    {
        "name": "Puede Ver Definicion de Meta por Filial",
        "content_type_name": "goals",
        "codename": "puede_ver_definicion_de_meta_por_filial",
    },
    {
        "name": "Puede Ver Detalle Filial",
        "content_type_name": "goals",
        "codename": "puede_ver_detalle_filial",
    },
    {
        "name": "Puede Asignar Metas Globales",
        "content_type_name": "goals",
        "codename": "puede_asignar_metas_globales",
    },

    {
        "name": "Puede Ingresar Definiciones Manuales",
        "content_type_name": "goals",
        "codename": "puede_ingresar_definiciones_manuales",
    },
    {
        "name": "Puede Ingresar Ejecuciones Manuales",
        "content_type_name": "goals",
        "codename": "puede_ingresar_ejecuciones_manuales",
    },
    {
        "name": "Puede Listar Metas",
        "content_type_name": "goals",
        "codename": "puede_listar_metas",
    },
    {
        "name": "Puede Ingresar Metas",
        "content_type_name": "goals",
        "codename": "puede_ingresar_metas",
    },
    {
        "name": "Puede Editar Metas",
        "content_type_name": "goals",
        "codename": "puede_editar_metas",
    },
    {
        "name": "Puede Eliminar Metas",
        "content_type_name": "goals",
        "codename": "puede_eliminar_metas",
    },
    {
        "name": "Puede Ver Metas de Centros de Costos Asignados",
        "content_type_name": "goals",
        "codename": "puede_ver_metas_centros_costos_asignadas",
    },
    {
        "name": "Puede Ver Metas de Todos los Centros de Costos",
        "content_type_name": "goals",
        "codename": "puede_ver_metas_todos_centros_costos",
    }
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
    + master_budget
    + goals_permissions
)
