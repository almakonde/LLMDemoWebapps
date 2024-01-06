from flask import Flask, request, render_template
from summarizer.sbert import SBertSummarizer
import logging

# Инициализация Flask приложения
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация модели Summarizer
model = SBertSummarizer('paraphrase-MiniLM-L6-v2')

@app.route("/")
def msg():
    # Отображение главной страницы
    return render_template('index.html')

@app.route("/generate_text", methods=['POST'])
def getSummary():
    try:
        # Проверка и получение входных данных
        body = request.form['data']
        if not body:
            # Генерация исключения, если текст не предоставлен
            raise ValueError("Текст для резюмирования не предоставлен")

        # Генерация резюме
        result = model(body, num_sentences=5)

        # Возвращение результата в шаблон
        return render_template('summary.html', generated_text=result)
    except Exception as e:
        # Логирование ошибок
        logging.error("Произошла ошибка: %s", str(e))
        # Убедитесь, что у вас есть шаблон error.html
        return render_template('error.html', error=str(e))

if __name__ == "__main__":
    # Запуск приложения
    app.run(debug=True, port=7000)