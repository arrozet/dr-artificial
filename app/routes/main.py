from flask import Blueprint, render_template, request

main_bp = Blueprint("main", __name__)

#PARA QUE FUNCIONE EN INTERFAZ1 O INDEX CAMBIAR EN DONDE HE COMENTADO
@main_bp.route("/")
def home():
    return render_template("interfaz1.html") # AQUI


@main_bp.route('/', methods=['POST'])
def procesarPrompt():
    prompt = request.form['prompt']  # Elimina espacios en blanco

    mi_mensaje = f"""
        <div class="UserMessage">
            <div class="avatar user">U</div>
            <div class="message-content">
                <div class="message-bubble">
                    {prompt}
                </div>
            </div>
        </div>
        """

    respuesta = "HOLA"
    respuesta_html = f"""
        <div class="AiMessage">
            <div class="avatar">AI</div>
            <div class="message-content">
                <div class="message-bubble">
                    {respuesta}
                </div>
            </div>
        </div>
        """

    if not prompt:  # Validación para evitar enviar texto vacío
        return render_template('interfaz1.html', mensaje='No puedes enviar un texto vacío.') #AQUI

    return render_template('interfaz1.html', mi_mensaje=mi_mensaje, respuesta=respuesta_html) #AQUI

@main_bp.route('/<chat_name>')
def mostrar_chat(chat_name):
    return render_template(f'{chat_name}.html')