import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración general
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title(" University Data Dashboard")

# Cargar datos
df = pd.read_csv("university_student_data (2).csv")

# --- Filtros interactivos ---
st.sidebar.header("Filtros")
year = st.sidebar.selectbox("Año", sorted(df["Year"].unique()))
terms = st.sidebar.multiselect("Término(s)", df["Term"].unique(), default=df["Term"].unique())
df_f = df[(df["Year"] == year) & (df["Term"].isin(terms))]

# --- KPIs ---
col1, col2, col3 = st.columns(3)
col1.metric("Applications", int(df_f["Applications"].sum()))
col2.metric("Retention Avg (%)", f"{df_f['Retention Rate (%)'].mean():.1f}%")
col3.metric("Satisfaction Avg (%)", f"{df_f['Student Satisfaction (%)'].mean():.1f}%")

# --- Visualización 1: Retention trend ---
st.subheader("Tendencia Retention Rate (%) por Año")
fig1, ax1 = plt.subplots()
sns.lineplot(data=df.groupby("Year")["Retention Rate (%)"].mean().reset_index(),
             x="Year", y="Retention Rate (%)", marker="o", color="royalblue", ax=ax1)
ax1.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig1)

# --- Visualización 2: Student Satisfaction by Year ---
st.subheader("Student Satisfaction (%) por Año")
fig2, ax2 = plt.subplots()
sns.barplot(data=df.groupby("Year")["Student Satisfaction (%)"].mean().reset_index(),
            x="Year", y="Student Satisfaction (%)", hue="Year",
            palette="Blues_d", dodge=False, legend=False, ax=ax2)
ax2.set_ylim(0,100); ax2.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig2)

# --- Visualización 3: Distribución de matrícula entre Spring y Fall ---
st.subheader("Distribución de matrícula entre Spring y Fall")

# Asegurarse de recalcular la columna Total Enrolled con base en los datos filtrados (df_f)
facultades = [c for c in df_f.columns if "Enrolled" in c and "Total" not in c]
if facultades:
    df_f["Total Enrolled"] = df_f[facultades].sum(axis=1)
else:
    st.error("No se encontraron columnas con 'Enrolled' para crear 'Total Enrolled' en el filtro actual.")

# Agrupar por término (Spring/Fall) usando SOLO los datos filtrados
comp_term = df_f.groupby("Term", as_index=False)["Total Enrolled"].sum()

# Validar que existan datos
if not comp_term.empty and comp_term["Total Enrolled"].sum() > 0:
    fig3, ax3 = plt.subplots()
    ax3.pie(
        comp_term["Total Enrolled"],
        labels=comp_term["Term"],
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("pastel")
    )
    st.pyplot(fig3)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")



# --- Visualización 4: Tabla con datos filtrados ---
# Dejamos esta pequeña tabla como parte del dashboard para mostrar los datos filtrados en detalle.
# Sirve como referencia de transparencia y verificación de los valores usados en las gráficas y KPIs.
st.subheader("Datos filtrados según los criterios seleccionados")
st.dataframe(df_f, use_container_width=True)

