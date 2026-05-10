from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Métodos próprios de conversão

def converter_para_decimal(numero, base):
    """Converte um número de qualquer base para decimal manualmente"""
    numero = numero.upper()
    decimal = 0
    
    for i, digito in enumerate(reversed(numero)):
        # Converter caractere para valor numérico
        if digito.isdigit():
            valor = int(digito)
        else:
            valor = ord(digito) - ord('A') + 10
        
        # Validar se o dígito é válido para a base
        if valor >= base:
            raise ValueError(f"Dígito {digito} inválido para base {base}")
        
        decimal += valor * (base ** i)
    
    return decimal


def converter_de_decimal(numero_decimal, base):
    """Converte um número decimal para qualquer base manualmente"""
    if numero_decimal == 0:
        return '0'
    
    digitos = '0123456789ABCDEF'
    resultado = ''
    
    while numero_decimal > 0:
        resto = numero_decimal % base
        resultado = digitos[resto] + resultado
        numero_decimal = numero_decimal // base
    
    return resultado


# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página integrante
@app.route('/integrante')
def integrante():
    return render_template('integrante.html')

# Página conversor
@app.route('/conversor')
def conversor():
    return render_template('conversor.html')

# Função de conversão
@app.route('/converter', methods=['POST'])
def converter():

    numero = request.form['numero'].strip()
    origem = request.form['origem']
    destino = request.form['destino']

    try:
        # Mapear nomes de bases para valores numéricos
        bases = {
            'decimal': 10,
            'binario': 2,
            'hexadecimal': 16,
            'octal': 8
        }

        # Converter para decimal primeiro
        if origem == 'decimal':
            decimal = int(numero)
        else:
            decimal = converter_para_decimal(numero, bases[origem])

        # Converter para destino
        if destino == 'decimal':
            resultado = str(decimal)
        else:
            resultado = converter_de_decimal(decimal, bases[destino])

        return jsonify({'resultado': resultado})

    except ValueError as e:
        return jsonify({'resultado': 'Número inválido'})
    except:
        return jsonify({'resultado': 'Número inválido'})


if __name__ == '__main__':
    app.run(debug=True)