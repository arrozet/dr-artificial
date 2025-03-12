# Cargar los datos sin cabecera
datos_temp <- read.csv("datos_sinteticos/resumen_evolucion.csv", header = FALSE)

# Extraer los nombres de columnas de la primera fila
nombres_columnas <- as.character(datos_temp[1, ])

# Crear el dataframe final sin la primera fila
Resumen_Evolucion <- datos_temp[-1, ]

# Asignar los nombres de columnas correctos
colnames(Resumen_Evolucion) <- nombres_columnas

# Convertir todas las columnas que deberían ser numéricas
columnas_numericas <- c("PresionSistolica", "PresionDiastolica", "FrecuenciaCardiaca",
                        "Temperatura", "FrecuenciaRespiratoria", "SaturacionOxigeno",
                        "Glucosa", "Leucocitos", "Hemoglobina", "Plaquetas", "Colesterol",
                        "HDL", "LDL", "Trigliceridos", "Sodio", "Potasio", "ClNa", 
                        "Creatinina", "Urea", "AST", "ALT", "Bilirrubina", "pH", 
                        "pCO2", "pO2", "HCO3", "Lactato")

# Convertir las columnas a numéricas donde sea posible
for (col in columnas_numericas) {
  if (col %in% colnames(Resumen_Evolucion)) {
    Resumen_Evolucion[[col]] <- as.numeric(as.character(Resumen_Evolucion[[col]]))
  }
}

# Convertir PacienteID a factor para análisis categóricos
Resumen_Evolucion$PacienteID <- as.factor(Resumen_Evolucion$PacienteID)

# Convertir fechas a formato Date
Resumen_Evolucion$Fecha <- as.Date(Resumen_Evolucion$Fecha, format="%d/%m/%Y")

# Mostrar información sobre el dataframe resultante
str(Resumen_Evolucion)


#IMPORTANTE: Problema en el dataset por culpa de una columna extra en ciertas filas (no hay información sobre qué es esa columna, así
#que la vamos a borrar)

Resumen_Evolucion$`NA`=NULL

#El exceso de columnas también ha generado filas extra, por ejemplo la fila 18:
Resumen_Evolucion[18,]

