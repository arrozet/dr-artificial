from app import create_app
# PARA CAMBIAR EL PATH DE INICIO TIENES QUE IRTE A ROUTER -> MAIN.PY Y CAMBIARLA
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
