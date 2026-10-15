                        border: 1.5px solid {config_st['cor']};
                        border-radius: 999px;
                        background-color: {config_st['fundo']};
                        min-height: 36px;
                        padding: 0 14px;
                        cursor: pointer;
                        user-select: none;
                        margin-bottom: 25px;
                    ">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="width: 8px; height: 8px; background-color: {config_st['cor']}; border-radius: 50%; display: inline-block;"></span>
                            <span style="color: {config_st['cor']}; font-weight: 700; font-size: 0.85rem; font-family: sans-serif;">{config_st['label']}</span>
                        </div>
                        <span style="color: {config_st['cor']}; font-size: 0.75rem;">▼</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.selectbox(
                    "Alterar status",
                    STATUS,
                    index=STATUS.index(chamado["status"]),
                    key=f"select_acao_{chamado['id']}",
                    label_visibility="collapsed",
                    on_change=salvar_status,
                    args=(chamado["id"],),
                )

                st.markdown(
                    f"""
                    <style>
                    .st-key-select_acao_{chamado['id']} {{
                        margin-top: -61px !important;
                        opacity: 0.01 !important;
                        position: relative !important;
                        z-index: 10 !important;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                
                st.markdown(
                    f"""
                    <style>
                    .st-key-btn_detalhe_{chamado['id']} {{
                        margin-top: -15px !important;
                        display: flex !important;
                        justify-content: flex-end !important;
                        width: 100% !important;
                    }}
                    .st-key-btn_detalhe_{chamado['id']} [data-testid="stButton"] {{
                        width: auto !important;
                        display: flex !important;
                        justify-content: flex-end !important;
                    }}
                    .st-key-btn_detalhe_{chamado['id']} button {{
                        background-color: transparent !important;
                        border: none !important;
                        border-radius: 6px !important;
                        padding: 4px 10px !important;
                        color: #1769b0 !important;
                        font-family: sans-serif !important;
                        font-size: 0.8rem !important;
                        font-weight: 650 !important;
                        cursor: pointer !important;
                        box-shadow: none !important;
                        transition: all 0.15s ease !important;
                        width: auto !important;
                        min-height: auto !important;
                        display: inline-flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                        gap: 6px !important;
                        margin-left: auto !important;
                    }}
                    .st-key-btn_detalhe_{chamado['id']} button::before {{
                        content: "" !important;
                        display: inline-block !important;
                        width: 14px !important;
                        height: 14px !important;
                        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231769b0' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'></path><polyline points='14 2 14 8 20 8'></polyline><line x1='16' y1='13' x2='8' y2='13'></line><line x1='16' y1='17' x2='8' y2='17'></line><polyline points='10 9 9 9 8 9'></polyline></svg>") !important;
                        background-size: contain !important;
                        background-repeat: no-repeat !important;
                    }}
                    .st-key-btn_detalhe_{chamado['id']} button:hover {{
                        background-color: #f0f7ff !important;
                        color: #12548e !important;
                    }}
                    .st-key-btn_detalhe_{chamado['id']} button:hover::before {{
                        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2312548e' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z'></path><polyline points='14 2 14 8 20 8'></polyline><line x1='16' y1='13' x2='8' y2='13'></line><line x1='16' y1='17' x2='8' y2='17'></line><polyline points='10 9 9 9 8 9'></polyline></svg>") !important;
                    }}
                    .st-key-btn_detalhe_{chamado['id']} button p {{
                        color: inherit !important;
                        font-weight: 650 !important;
                        margin: 0 !important;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button("Ver detalhes", key=f"btn_detalhe_{chamado['id']}"):
                    st.session_state.chamado_detalhe_id = chamado["id"]
                    st.session_state.modal_minimized = False
                    st.session_state.modal_maximized = False
                    st.rerun()

with col_formulario:
    with st.container(border=True):
        st.subheader("Abrir novo chamado")
        st.caption("Preencha os dados abaixo para registrar uma nova solicitação.")
        with st.form("form_novo_chamado", clear_on_submit=True):
            titulo = st.text_input("Título do chamado *", placeholder="Ex.: Computador não liga")
            solicitante = st.text_input("Nome do solicitante *", placeholder="Nome completo")
            categoria = st.selectbox("Categoria", CATEGORIAS)
            prioridade = st.selectbox("Prioridade", PRIORIDADES, index=1)
            descricao = st.text_area("Descrição *", placeholder="Descreva o problema com o máximo de detalhes possível...", height=82)
            enviar = st.form_submit_button("➤  Registrar chamado", use_container_width=True)

        if enviar:
            if not titulo.strip() or not solicitante.strip() or not descricao.strip():
                st.error("Preencha a título, o nome do solicitante e a descrição.")
            else:
                criar_chamado(
                    titulo.strip(), solicitante.strip(), categoria,
