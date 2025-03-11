from flask import Blueprint, render_template, request

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route('/', methods=['POST'])
def procesarPrompt():
    prompt = request.form['prompt']  # Elimina espacios en blanco

    mi_mensaje = f"""
        <div class="message">
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
        <div class="message">
            <div class="avatar">AI</div>
            <div class="message-content">
                <div class="message-bubble">
                    {respuesta}
                </div>
            </div>
        </div>
        """

    if not prompt:  # Validación para evitar enviar texto vacío
        return render_template('index.html', mensaje='No puedes enviar un texto vacío.')

    return render_template('index.html', mi_mensaje=mi_mensaje, respuesta=respuesta_html)