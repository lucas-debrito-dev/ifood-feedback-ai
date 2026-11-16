
import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO
st.set_page_config(
    page_title="iFood Feedback AI",
    page_icon="🍔",
    layout="wide"
)

# DADOS DEMONSTRATIVOS
dados = {
    "Cliente": [
        "Cliente 01", "Cliente 02", "Cliente 03",
        "Cliente 04", "Cliente 05", "Cliente 06",
        "Cliente 07", "Cliente 08", "Cliente 09",
        "Cliente 10", "Cliente 11", "Cliente 12"
    ],
    "Avaliação": [5, 2, 4, 1, 5, 3, 2, 5, 4, 1, 3, 5],
    "Comentário": [
        "Entrega rápida e comida excelente",
        "Pedido chegou atrasado",
        "Muito bom, recomendo",
        "Comida chegou fria",
        "Excelente atendimento",
        "Entrega dentro do prazo",
        "Pedido veio errado",
        "Adorei a experiência",
        "Comida saborosa",
        "Demora excessiva na entrega",
        "Atendimento poderia melhorar",
        "Tudo perfeito!"
    ],
    "Sentimento": [
        "Positivo", "Negativo", "Positivo",
        "Negativo", "Positivo", "Positivo",
        "Negativo", "Positivo", "Positivo",
        "Negativo", "Negativo", "Positivo"
    ],
    "Categoria": [
        "Entrega", "Entrega", "Qualidade",
        "Qualidade", "Atendimento", "Entrega",
        "Pedido", "Qualidade", "Qualidade",
        "Entrega", "Atendimento", "Qualidade"
    ]
}

df = pd.DataFrame(dados)

# IMPORTAÇÃO DE ARQUIVO CSV
st.sidebar.header("Importar avaliações")

arquivo = st.sidebar.file_uploader(
    "Envie uma planilha CSV",
    type=["csv"]
)


if arquivo is not None:
    try:
        df_importado = pd.read_csv(arquivo)

        colunas_obrigatorias = [
            "Cliente",
            "Avaliação",
            "Comentário",
            "Sentimento",
            "Categoria"
        ]

        faltando = [
            coluna for coluna in colunas_obrigatorias
            if coluna not in df_importado.columns
        ]

        if faltando:
            st.sidebar.error(
                f"Colunas ausentes: {', '.join(faltando)}"
            )
            st.stop()

        df = df_importado

    except Exception as erro:
        st.sidebar.error(f"Erro ao ler arquivo: {erro}")
        st.stop()


# ANÁLISE AUTOMÁTICA DE SENTIMENTOS


def analisar_sentimento(comentario):
    texto = str(comentario).lower()

    # EXPRESSÕES POSITIVAS
    expressoes_positivas = [
        "entrega rápida",
        "entrega rapida",
        "comida excelente",
        "muito bom",
        "excelente atendimento",
        "adorei a experiência",
        "comida saborosa",
        "entrega dentro do prazo",
        "tudo perfeito",
        "super recomendo"
    ]

    # EXPRESSÕES NEGATIVAS
    expressoes_negativas = [
        "pedido chegou atrasado",
        "comida chegou fria",
        "comida fria",
        "pedido veio errado",
        "demora excessiva",
        "atendimento poderia melhorar",
        "não gostei",
        "nao gostei",
        "não recomendo",
        "nao recomendo",
        "muito ruim",
        "péssimo atendimento",
        "pessimo atendimento",
        "produto estragado"
    ]

    positivas = 0
    negativas = 0

    # Identifica expressões positivas sem contar palavras repetidas
    for expressao in expressoes_positivas:
        if expressao in texto:
            positivas += 1
            texto = texto.replace(expressao, "", 1)

    # Identifica expressões negativas
    for expressao in expressoes_negativas:
        if expressao in texto:
            negativas += 1
            texto = texto.replace(expressao, "", 1)

    # PALAVRAS POSITIVAS
    palavras_positivas = [
        "adorei", "ótimo", "otimo", "excelente",
        "bom", "boa", "rápido", "rapido",
        "satisfeito", "gostei", "perfeito",
        "saborosa", "recomendo"
    ]

    # PALAVRAS NEGATIVAS
    palavras_negativas = [
        "ruim", "péssimo", "pessimo", "atrasado",
        "demora", "problema", "problemas",
        "reclamação", "reclamacao", "insatisfeito",
        "defeito", "horrível", "horrivel",
        "fria", "errado"
    ]

    positivas += sum(
        palavra in texto
        for palavra in palavras_positivas
    )

    negativas += sum(
        palavra in texto
        for palavra in palavras_negativas
    )

    if positivas > negativas:
        return "Positivo"
    elif negativas > positivas:
        return "Negativo"
    else:
        return "Neutro"
df["Sentimento automático"] = df["Comentário"].apply(analisar_sentimento)



# CABEÇALHO
st.title("🍔 iFood Feedback AI")
st.subheader("Inteligência de dados para experiência do cliente")

st.caption(
    "Projeto independente de portfólio | "
    "Dados fictícios para demonstração"
)

st.divider()

# FILTROS
st.sidebar.header("Filtros")

sentimentos_disponiveis = sorted(df["Sentimento"].dropna().unique())

categorias_disponiveis = sorted(df["Categoria"].dropna().unique())

sentimentos = st.sidebar.multiselect(
    "Filtrar sentimentos",
    options=sentimentos_disponiveis,
    default=sentimentos_disponiveis,
    key="filtro_sentimentos"
)

categorias = st.sidebar.multiselect(
    "Filtrar categorias",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
    key="filtro_categorias"
)

df_filtrado = df[
    (df["Sentimento"].isin(sentimentos)) &
    (df["Categoria"].isin(categorias))
]

# INDICADORES
st.subheader("Indicadores gerais")

total = len(df_filtrado)

positivas = (
    df_filtrado["Sentimento"].eq("Positivo").sum()
)

negativas = (
    df_filtrado["Sentimento"].eq("Negativo").sum()
)

percentual_positivo = (
    positivas / total * 100 if total > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Avaliações", total)

col2.metric(
    "Positivas",
    positivas,
    f"{percentual_positivo:.1f}% do total" if total else "0%"
)

col3.metric("Negativas", negativas)

col4.metric(
    "Nota média",
    f"{df_filtrado['Avaliação'].mean():.1f}/5"
    if total else "Sem dados"
)

st.divider()

# RESULTADO DA ANÁLISE DE SENTIMENTOS

st.subheader("Análise automática de sentimentos")

st.caption(
    "Comparação entre o sentimento informado "
    "e o sentimento identificado pelo sistema."
)

st.dataframe(
    df_filtrado[
        [
            "Comentário",
            "Sentimento",
            "Sentimento automático"
        ]
    ],
    width="stretch",
    hide_index=True
)

# INDICADOR DE CONCORDÂNCIA

st.subheader("Desempenho do classificador")

if not df_filtrado.empty:
    concordancias = (
        df_filtrado["Sentimento"]
        == df_filtrado["Sentimento automático"]
    ).sum()

    total_comparacoes = len(df_filtrado)

    taxa_concordancia = (
        concordancias / total_comparacoes
    ) * 100

    st.metric(
        "Concordância entre classificações",
        f"{taxa_concordancia:.1f}%",
        f"{concordancias} de {total_comparacoes} avaliações"
    )
else:
    st.info("Não há avaliações para comparar.")

# RECOMENDAÇÕES AUTOMÁTICAS

st.divider()
st.subheader("Recomendações para o negócio")

negativas_por_categoria = (
    df[df["Sentimento automático"] == "Negativo"]
    .groupby("Categoria")
    .size()
    .sort_values(ascending=False)
)

if not negativas_por_categoria.empty:

    categoria_critica = negativas_por_categoria.index[0]
    quantidade = negativas_por_categoria.iloc[0]

    st.warning(
        f"A categoria '{categoria_critica}' "
        f"concentra {quantidade} avaliação(ões) negativa(s)."
    )

    st.write(
        f"**Recomendação:** investigar possíveis problemas "
        f"relacionados a {categoria_critica.lower()} "
        f"e avaliar melhorias nesse processo."
    )

else:
    st.success(
        "Nenhuma avaliação negativa foi identificada. "
        "Continue acompanhando a experiência dos clientes."
    )


# GRÁFICOS
st.subheader("Análise dos feedbacks")

grafico1, grafico2 = st.columns(2)

with grafico1:
    contagem = (
        df_filtrado["Sentimento"]
        .value_counts()
        .rename_axis("Sentimento")
        .reset_index(name="Quantidade")
    )

    fig_sentimentos = px.pie(
        contagem,
        names="Sentimento",
        values="Quantidade",
        title="Distribuição dos sentimentos",
        hole=0.45
    )

    st.plotly_chart(
        fig_sentimentos,
        width="stretch"
    )

with grafico2:
    contagem_categoria = (
        df_filtrado["Categoria"]
        .value_counts()
        .rename_axis("Categoria")
        .reset_index(name="Quantidade")
    )

    fig_categorias = px.bar(
        contagem_categoria,
        x="Categoria",
        y="Quantidade",
        title="Feedbacks por categoria",
        text="Quantidade"
    )

    st.plotly_chart(
        fig_categorias,
        width="stretch"
    )

st.divider()

# TABELA DE AVALIAÇÕES
st.subheader("Avaliações dos clientes")

st.dataframe(
    df_filtrado,
    width="stretch",
    hide_index=True
)

# INSIGHTS INICIAIS
st.subheader("💡 Insights")

if total > 0:
    categoria_critica = (
        df_filtrado[
            df_filtrado["Sentimento"] == "Negativo"
        ]["Categoria"].value_counts()
    )

    if not categoria_critica.empty:
        st.warning(
            f"Categoria com mais reclamações: "
            f"{categoria_critica.index[0]}."
        )
    else:
        st.success(
            "Nenhuma avaliação negativa encontrada nos filtros atuais."
        )
else:
    st.info("Nenhuma avaliação encontrada com os filtros selecionados.")

st.caption(
    "iFood Feedback AI | Desenvolvido por Lucas de Brito | "
    "Projeto acadêmico independente"
)
