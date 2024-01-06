from flask import Flask, request, render_template
import openai
import logging

# Set your OpenAI API key here
openai.api_key = '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'

# Initialization of Flask application
app = Flask(__name__)

@app.route("/")
def msg():
    # Display the main page
    return render_template('index.html')

@app.route("/generate_text", methods=['POST'])
def generate_text():
    try:
        # Check and get input data
        user_input = request.form['data']
        if not user_input:
            raise ValueError("Text prompt is not provided")

        # Use GPT-4 chat completions API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Adjust the model name as needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=3800,  # Adjust max_tokens based on your desired generated text length
            top_p=1,
        )

        # Extract the generated text from the API response
        generated_text = response['choices'][0]['message']['content']

        # Return the result to the template
        return render_template('summary.html', generated_text=generated_text)
    except Exception as e:
        # Log errors
        logging.error("An error occurred: %s", str(e))
        # Make sure you have an 'error.html' template
        return render_template('error.html', error=str(e))

if __name__ == "__main__":
    # Run the application
    app.run(debug=True, port=5000)
