import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Dashboard de Vendas | Notebooks",
    page_icon=":material/monitoring:",
    layout="wide",
    initial_sidebar_state="expanded",
)

COR_FUNDO = "#FBF7F0"
COR_CARD = "#FFFFFF"
COR_BORDA = "#E4D7C1"
COR_TEXTO = "#3C2E1F"
COR_TEXTO_SUAVE = "#7A6A55"
COR_ACENTO = "#A9784F"
PALETA_GRAFICOS = ["#A9784F", "#C9A876", "#8B6F47", "#D9C4A0", "#6B5537", "#E8D5B5", "#5C4630"]


st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Poppins', sans-serif;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }}

        /* Cabeçalho estilo "hero" */
        .hero {{
            display: flex;
            align-items: center;
            gap: 0.9rem;
            margin-bottom: 0.2rem;
        }}
        .hero-icon {{
            font-size: 2.1rem;
            background-color: {COR_ACENTO}22;
            color: {COR_ACENTO};
            border-radius: 14px;
            padding: 0.5rem 0.65rem;
            display: flex;
        }}
        .hero-title {{
            font-size: 2.1rem;
            font-weight: 700;
            color: {COR_TEXTO};
            margin: 0;
            letter-spacing: -0.5px;
        }}
        .hero-subtitle {{
            color: {COR_TEXTO_SUAVE};
            font-size: 0.98rem;
            margin-top: 0.15rem;
        }}

        /* Cards de métrica customizados */
        .kpi-card {{
            background-color: {COR_CARD};
            border: 1px solid {COR_BORDA};
            border-left: 4px solid {COR_ACENTO};
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 2px 10px rgba(60, 46, 31, 0.05);
            height: 100%;
        }}
        .kpi-label {{
            color: {COR_TEXTO_SUAVE};
            font-size: 0.82rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 0.3rem;
        }}
        .kpi-value {{
            color: {COR_TEXTO};
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1.2;
        }}
        .kpi-delta {{
            color: {COR_ACENTO};
            font-size: 0.8rem;
            font-weight: 500;
            margin-top: 0.25rem;
        }}

        h2, h3 {{
            color: {COR_TEXTO};
            font-weight: 600;
        }}

        div[data-testid="stTabs"] button {{
            font-weight: 500;
            font-size: 0.95rem;
        }}

        section[data-testid="stSidebar"] {{
            border-right: 1px solid {COR_BORDA};
        }}

        .footer-note {{
            text-align: center;
            color: {COR_TEXTO_SUAVE};
            font-size: 0.8rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid {COR_BORDA};
        }}
    </style>
""", unsafe_allow_html=True)


def kpi_card(col, label, value, delta=None):
    """Renderiza um card de métrica customizado (mais 'site', menos 'widget padrão')."""
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


@st.cache_data
def carregar_dados():
    return pd.read_excel("Dados.xlsx")

try:
    dados_original = carregar_dados()
except FileNotFoundError:
    st.error("⚠️ Arquivo 'Dados.xlsx' não encontrado. Coloque-o na mesma pasta do script.")
    st.stop()


st.markdown("""
    <div class="hero">
        <div class="hero-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"
                 fill="none" stroke="currentColor" stroke-width="2"
                 stroke-linecap="round" stroke-linejoin="round">
                <rect width="7" height="9" x="3" y="3" rx="1"/>
                <rect width="7" height="5" x="14" y="3" rx="1"/>
                <rect width="7" height="9" x="14" y="12" rx="1"/>
                <rect width="7" height="5" x="3" y="16" rx="1"/>
            </svg>
        </div>
        <div>
            <p class="hero-title">Dashboard</p>
            <p class="hero-subtitle">Comparativo dos principais notebooks vendidos no Mercado Livre</p>
        </div>
    </div>
    <br>
""", unsafe_allow_html=True)

st.sidebar.markdown("### :material/filter_alt: Filtros")

fabricantes = st.sidebar.multiselect(
    "Empresas",
    options=sorted(dados_original["FABRICANTE"].unique()),
)

busca_produto = st.sidebar.text_input(":material/search: Buscar produto")

valor_min, valor_max = float(dados_original["TOTAL"].min()), float(dados_original["TOTAL"].max())
faixa_valor = st.sidebar.slider(
    "Faixa de valor (R$)",
    min_value=valor_min,
    max_value=valor_max,
    value=(valor_min, valor_max),
)

ordenar_por = st.sidebar.selectbox(
    "Ordenar ranking por",
    options=["Receita Total", "Quantidade Vendida"],
)

if st.sidebar.button(":material/restart_alt: Limpar filtros", use_container_width=True):
    st.rerun()

dados = dados_original.copy()

if fabricantes:
    dados = dados[dados["FABRICANTE"].isin(fabricantes)]

if busca_produto:
    dados = dados[dados["PRODUTO"].str.contains(busca_produto, case=False, na=False)]

dados = dados[(dados["TOTAL"] >= faixa_valor[0]) & (dados["TOTAL"] <= faixa_valor[1])]

st.sidebar.markdown("---")
st.sidebar.metric(":material/domain: Empresas no filtro", dados["FABRICANTE"].nunique())
st.sidebar.metric(":material/inventory_2: Produtos no filtro", len(dados))

if dados.empty:
    st.warning("Nenhum resultado para os filtros selecionados.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)

fabricante_top = dados.groupby("FABRICANTE")["TOTAL"].sum().idxmax()
share_top = dados.groupby("FABRICANTE")["TOTAL"].sum().max() / dados["TOTAL"].sum() * 100
mais_vendido = dados.loc[dados["QUANTIDADE"].idxmax()]

kpi_card(col1, "Receita Bruta", f"R$ {dados['TOTAL'].sum():,.2f}")
kpi_card(col2, "Ticket Médio", f"R$ {dados['TOTAL'].mean():,.2f}")
kpi_card(col3, "Unidades Vendidas", f"{int(dados['QUANTIDADE'].sum()):,}")
kpi_card(col4, "Líder de Mercado", fabricante_top, delta=f"{share_top:.1f}% da receita")

st.write("")

tab1, tab2, tab3 = st.tabs([
    ":material/bar_chart: Visão Geral",
    ":material/emoji_events: Ranking",
    ":material/table_view: Dados Detalhados",
])

with tab1:
    c1, c2 = st.columns([1.4, 1])

    with c1:
        st.markdown("##### Receita total por fabricante")
        receita_fab = (
            dados.groupby("FABRICANTE")["TOTAL"].sum().sort_values(ascending=True).reset_index()
        )
        fig_bar = px.bar(
            receita_fab, x="TOTAL", y="FABRICANTE", orientation="h",
            color="TOTAL", color_continuous_scale=PALETA_GRAFICOS,
            labels={"TOTAL": "Receita (R$)", "FABRICANTE": ""},
        )
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color=COR_TEXTO, coloraxis_showscale=False,
            margin=dict(l=0, r=10, t=10, b=10), height=380,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        st.markdown("##### Participação na receita")
        fig_pie = px.pie(
            receita_fab, values="TOTAL", names="FABRICANTE", hole=0.55,
            color_discrete_sequence=PALETA_GRAFICOS,
        )
        fig_pie.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color=COR_TEXTO, showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10), height=380,
        )
        fig_pie.update_traces(textinfo="percent+label", textfont_size=11)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("##### Ticket médio por fabricante")
    ticket_fab = dados.groupby("FABRICANTE")["TOTAL"].mean().sort_values(ascending=False).reset_index()
    fig_line = px.line(ticket_fab, x="FABRICANTE", y="TOTAL", markers=True)
    fig_line.update_traces(line_color=COR_ACENTO, marker_color=COR_ACENTO)
    fig_line.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color=COR_TEXTO, yaxis_title="Ticket médio (R$)", xaxis_title="",
        margin=dict(l=0, r=10, t=10, b=10), height=320,
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    coluna_ordenacao = "TOTAL" if ordenar_por == "Receita Total" else "QUANTIDADE"
    ranking = (
        dados.groupby("FABRICANTE")
        .agg(Receita_Total=("TOTAL", "sum"), Unidades=("QUANTIDADE", "sum"))
        .reset_index()
        .sort_values("Receita_Total" if ordenar_por == "Receita Total" else "Unidades", ascending=False)
    )
    ranking["Participação (%)"] = (ranking["Receita_Total"] / ranking["Receita_Total"].sum() * 100).round(1)

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True,
        column_config={
            "FABRICANTE": "Fabricante",
            "Receita_Total": st.column_config.NumberColumn("Receita Total", format="R$ %.2f"),
            "Unidades": st.column_config.NumberColumn("Unidades Vendidas"),
            "Participação (%)": st.column_config.ProgressColumn(
                "Participação (%)", format="%.1f%%", min_value=0, max_value=float(ranking["Participação (%)"].max()),
            ),
        },
    )

    st.markdown("##### Top 5 produtos mais vendidos")
    top5 = dados.sort_values("QUANTIDADE", ascending=False).head(5)[["PRODUTO", "FABRICANTE", "QUANTIDADE", "TOTAL"]]
    st.dataframe(
        top5, use_container_width=True, hide_index=True,
        column_config={
            "PRODUTO": "Produto", "FABRICANTE": "Fabricante",
            "QUANTIDADE": st.column_config.NumberColumn("Unidades"),
            "TOTAL": st.column_config.NumberColumn("Receita (R$)", format="R$ %.2f"),
        },
    )

with tab3:
    st.markdown("##### Base de dados filtrada")
    st.dataframe(dados, use_container_width=True, hide_index=True)

    csv = dados.to_csv(index=False).encode("utf-8")
    st.download_button(
        ":material/download: Baixar dados filtrados (CSV)",
        data=csv, file_name="dados_filtrados.csv", mime="text/csv",
    )

st.markdown('<div class="footer-note">Dashboard atualizado automaticamente a partir de Dados.xlsx</div>', unsafe_allow_html=True)